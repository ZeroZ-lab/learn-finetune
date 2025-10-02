# 模块 5：RAG 全链路开发（CO4）

本模块讲解可上线的 RAG 体系：分块与元数据设计、向量检索与 BM25 融合、Cross‑Encoder 重排、引用对齐与冷热分层、评估与性能目标。示例内置本地 TF‑IDF 回退，便于零依赖演示；生产建议接入 Milvus。

学习目标（对齐 CO4）
- 设计高质量分块与元数据；理解 Schema 与索引选择的取舍。
- 构建 Hybrid（Dense + Sparse）检索与 Cross‑Encoder 重排；实现引用对齐。
- 使用 Ragas/DeepEval 评估 Faithfulness 与 Answer Relevance，使指标较纯生成提升 ≥20%。

目录与示例
- retrievers.py：本地 TF‑IDF 检索；MilvusRetriever 集成（支持向量库接入）。
- rerankers.py：简单重排（长度惩罚示例）。
- app/ingest.py：导入与索引构建（本地演示）。
- app/ask.py：查询（检索 + 重排 + 引用占位）。
- samples.txt：示例语料。

快速运行（本地回退，不依赖 Milvus）
```
pip install scikit-learn nltk
python modules/05-rag-system/app/ingest.py --docs modules/05-rag-system/samples.txt --index data/index.pkl
python modules/05-rag-system/app/ask.py --index data/index.pkl --query "介绍一下示例文档"
```

1. 分块与元数据（Chunking & Metadata）
- 分块策略：固定长度、递归分块（保留语义边界）、基于标题/段落。
- 元数据：来源、标题、页码/位置、时间戳、权限标签；为过滤与引用对齐提供依据。

2. 向量库与 Hybrid 检索
- 向量库选择：Milvus（HNSW/IVF）、Qdrant、Weaviate；离线/托管权衡。
- Hybrid：Dense（语义） + Sparse（BM25/TF‑IDF） → RRF 融合提升稳健性。
- 过滤表达式：基于元数据做子集检索（如产品/地区/时间范围）。

3. 重排与引用对齐
- Cross‑Encoder 重排：对 query‑passage 逐对打分，显著提升前列质量。
- 引用对齐：在返回的回答中附上引用的 chunk_id 或原文位置，便于审核与溯源。

4. 冷热分层与缓存
- 高频问题与高价值文档放入「热层」；低频归档到「冷层」。
- 缓存近似最近请求（embedding 相似）与最终回答，降低延迟与成本。

5. 评估与目标
- Ragas 指标：Faithfulness / Answer Relevance / Context Precision / Context Recall。
- 性能：P99 <500ms（在给定硬件/规模下）；观察超时率与错误率。

6. 常见坑位
- 过度/不足分块：过大降低召回，过小增加噪音；需要任务驱动的调参。
- 无监督嵌入选择不当：确保中英文语料匹配（如 bge‑m3/gte/e5）。
- 只做 Dense：引入 BM25 提升鲁棒性；企业内网常见「术语型」关键词。

7. 接入 Milvus（示例实现）
- 依赖：`pip install pymilvus`；`MilvusRetriever` 默认创建 `doc_id/embedding/text/metadata` Schema。
- `ingest` 需提供包含 `embedding` 的 `Document.meta`，便于与你的嵌入流水线衔接。
- 默认索引：HNSW + Cosine，可通过参数自定义；`save/load` 支持在批处理脚本与 API 服务间共享配置。
- 混合检索：
  - 向量检索得分已转换为相似度（Cosine → 1 - distance）。
  - 可与 BM25/RRF 融合 → 候选→Cross‑Encoder 重排→生成。

8. 参考资料

学习路径（循序渐进）
- lessons/01-chunking-metadata.md：分块与元数据
- lessons/02-embedding-selection.md：Embedding 与度量
- lessons/03-hybrid-retrieval.md：Hybrid 融合
- lessons/04-rerank-citations.md：重排与引用对齐
- lessons/05-evaluation.md：Ragas 评估
- lessons/06-performance.md：性能与缓存
- RAGAS 文档与示例
- Milvus 官方文档与 Schema/索引最佳实践
- bge‑m3 / gte / e5 嵌入模型说明
