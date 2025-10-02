from __future__ import annotations

import json
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

try:  # optional dependency – only required when using Milvus
    from pymilvus import (
        Collection,
        CollectionSchema,
        DataType,
        FieldSchema,
        connections,
        utility,
    )
except ImportError:  # pragma: no cover - pymilvus 在默认环境中可能不存在
    Collection = None  # type: ignore
    CollectionSchema = None  # type: ignore
    DataType = None  # type: ignore
    FieldSchema = None  # type: ignore
    connections = None  # type: ignore
    utility = None  # type: ignore


@dataclass
class Document:
    doc_id: str
    text: str
    meta: dict


class LocalTfidfRetriever:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=20000)
        self.doc_ids: list[str] = []
        self.meta: list[dict] = []
        self.matrix = None

    def ingest(self, docs: List[Document]):
        self.doc_ids = [d.doc_id for d in docs]
        self.meta = [d.meta for d in docs]
        texts = [d.text for d in docs]
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float, dict]]:
        if self.matrix is None:
            raise RuntimeError("index not built")
        q = self.vectorizer.transform([query])
        sims = linear_kernel(q, self.matrix).ravel()
        idx = sims.argsort()[::-1][:top_k]
        return [(
            self.doc_ids[i],
            float(sims[i]),
            self.meta[i],
        ) for i in idx]

    def save(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({
                "vectorizer": self.vectorizer,
                "doc_ids": self.doc_ids,
                "meta": self.meta,
                "matrix": self.matrix,
            }, f)

    @staticmethod
    def load(path: str) -> "LocalTfidfRetriever":
        with open(path, "rb") as f:
            obj = pickle.load(f)
        inst = LocalTfidfRetriever()
        inst.vectorizer = obj["vectorizer"]
        inst.doc_ids = obj["doc_ids"]
        inst.meta = obj["meta"]
        inst.matrix = obj["matrix"]
        return inst


class MilvusRetriever:
    """Milvus 检索实现，支持最小可复现的向量检索流程。

    设计约定：
    - 仅依赖 `pymilvus`，默认采用 FLOAT_VECTOR + JSON 元数据 Schema；
    - `docs` 的 `meta` 中需要包含 `embedding`（List[float]），通常由外部嵌入模型生成；
    - 通过 `save`/`load` 记录连接配置，便于离线脚本与服务共享。
    """

    def __init__(
        self,
        uri: str,
        user: str | None = None,
        password: str | None = None,
        *,
        collection_name: str = "rag_documents",
        dim: int = 768,
        index_params: Dict | None = None,
        search_params: Dict | None = None,
        recreate: bool = False,
        alias: str = "rag",
    ) -> None:
        if connections is None:
            raise ImportError(
                "pymilvus is required to use MilvusRetriever. Install with `pip install pymilvus`."
            )

        self.uri = uri
        self.user = user
        self.password = password
        self.collection_name = collection_name
        self.dim = dim
        self.index_params = index_params or {
            "metric_type": "COSINE",
            "index_type": "HNSW",
            "params": {"M": 32, "efConstruction": 200},
        }
        self.search_params = search_params or {
            "metric_type": "COSINE",
            "params": {"ef": 128},
        }
        self.metric_type = str(self.search_params.get("metric_type", "COSINE")).upper()
        self.alias = alias

        connections.connect(
            alias=self.alias,
            uri=self.uri,
            user=self.user,
            password=self.password,
        )

        if recreate and utility.has_collection(self.collection_name, using=self.alias):
            utility.drop_collection(self.collection_name, using=self.alias)

        self.collection = self._ensure_collection()

    def _ensure_collection(self) -> Collection:
        if not utility.has_collection(self.collection_name, using=self.alias):
            schema = CollectionSchema(
                fields=[
                    FieldSchema(
                        name="doc_id",
                        dtype=DataType.VARCHAR,
                        is_primary=True,
                        max_length=128,
                        description="Document identifier",
                    ),
                    FieldSchema(
                        name="embedding",
                        dtype=DataType.FLOAT_VECTOR,
                        dim=self.dim,
                        description="Embedding vector",
                    ),
                    FieldSchema(
                        name="text",
                        dtype=DataType.VARCHAR,
                        max_length=65535,
                        description="Original document text",
                    ),
                    FieldSchema(
                        name="metadata",
                        dtype=DataType.JSON,
                        description="Additional metadata",
                    ),
                ],
                description="RAG documents",
            )
            collection = Collection(
                name=self.collection_name,
                schema=schema,
                using=self.alias,
                consistency_level="Session",
            )
            collection.create_index("embedding", index_params=self.index_params)
        else:
            collection = Collection(self.collection_name, using=self.alias)
            if not collection.indexes:
                collection.create_index("embedding", index_params=self.index_params)

        return collection

    def ingest(self, docs: Iterable[Document], *, embedding_field: str = "embedding") -> None:
        """导入文档到 Milvus。

        Args:
            docs: 包含 text/meta 的 Document 序列，meta 中需包含 embedding。
            embedding_field: meta 中 embedding 的键名，默认为 "embedding"。
        """

        doc_ids: List[str] = []
        vectors: List[List[float]] = []
        texts: List[str] = []
        metadatas: List[dict] = []

        for doc in docs:
            embedding = doc.meta.get(embedding_field)
            if embedding is None:
                raise ValueError(
                    f"Document {doc.doc_id} missing embedding under key '{embedding_field}'"
                )
            if len(embedding) != self.dim:
                raise ValueError(
                    f"Embedding dimension mismatch for {doc.doc_id}: expected {self.dim}, got {len(embedding)}"
                )
            doc_ids.append(doc.doc_id)
            vectors.append(list(map(float, embedding)))
            texts.append(doc.text)

            meta_copy = dict(doc.meta)
            meta_copy.pop(embedding_field, None)
            metadatas.append(meta_copy)

        if not doc_ids:
            return

        data = [doc_ids, vectors, texts, metadatas]
        self.collection.insert(data, timeout=60)
        self.collection.flush()

    def search(
        self,
        query_embedding: List[float],
        *,
        top_k: int = 5,
        output_fields: Tuple[str, ...] = ("doc_id", "text", "metadata"),
    ) -> List[Tuple[str, float, dict]]:
        """向量检索。

        Args:
            query_embedding: 查询的向量表示。
            top_k: 返回的候选数量。
            output_fields: 需要返回的字段，用于还原元数据。
        Returns:
            (doc_id, score, metadata) 列表；metadata 含 text/额外信息。
        """

        if len(query_embedding) != self.dim:
            raise ValueError(
                f"Query embedding dimension mismatch: expected {self.dim}, got {len(query_embedding)}"
            )

        search_res = self.collection.search(  # type: ignore[arg-type]
            data=[list(map(float, query_embedding))],
            anns_field="embedding",
            param=self.search_params,
            limit=top_k,
            output_fields=list(output_fields),
            consistency_level="Session",
        )

        hits = []
        for hit in search_res[0]:
            distance = float(hit.distance)
            if self.metric_type == "COSINE":
                score = 1.0 - distance
            else:
                score = -distance
            meta = {
                "text": hit.entity.get("text", ""),
                **(hit.entity.get("metadata") or {}),
            }
            hits.append((hit.entity.get("doc_id"), score, meta))
        return hits

    def save(self, path: str) -> None:
        """保存连接配置，便于脚本间共享。"""

        Path(path).parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "uri": self.uri,
            "user": self.user,
            "password": self.password,
            "collection_name": self.collection_name,
            "dim": self.dim,
            "index_params": self.index_params,
            "search_params": self.search_params,
            "alias": self.alias,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(config_path: str) -> "MilvusRetriever":
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return MilvusRetriever(
            uri=cfg["uri"],
            user=cfg.get("user"),
            password=cfg.get("password"),
            collection_name=cfg.get("collection_name", "rag_documents"),
            dim=cfg.get("dim", 768),
            index_params=cfg.get("index_params"),
            search_params=cfg.get("search_params"),
            alias=cfg.get("alias", "rag"),
        )

