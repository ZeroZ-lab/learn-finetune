# 03｜Hybrid：Dense + BM25 融合

目标
- 结合语义检索与关键词检索，提升鲁棒性。

要点
- 稀疏（BM25/TF‑IDF）对术语/符号敏感；Dense 对语义相似敏感。
- RRF 融合：将两个排序的 reciprocal ranks 相加排序。

实践
- 使用本地 TF‑IDF 回退 +（可选）向量检索实现简单融合。

