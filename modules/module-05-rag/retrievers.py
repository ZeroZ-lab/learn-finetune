from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


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
    """占位：接入 Milvus 的检索实现。

    需要实现：
    - ingest(docs)
    - search(query, top_k)
    - save/load（如需本地缓存连接/配置）
    """

    def __init__(self, uri: str, user: str | None = None, password: str | None = None):
        raise NotImplementedError("Implement Milvus integration here")

