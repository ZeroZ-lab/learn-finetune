# 04｜重排与引用对齐

目标
- 使用 Cross‑Encoder 提升前列文档质量；返回可追溯引用。

要点
- Cross‑Encoder 逐对打分，精度高但较慢；常用于前 k 的 rerank。
- 引用对齐：返回 chunk_id/offset；前端展示可跳转定位。

