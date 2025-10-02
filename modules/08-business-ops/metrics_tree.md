# 指标体系（示例）

- 效果（Quality）
  - 任务指标：Accuracy/F1/BLEU/ROUGE
  - RAG 指标：Faithfulness、Answer Relevance
  - Agent 指标：端到端成功率、工具调用成功率
- 效率（Efficiency）
  - QPS、P95/P99 延迟、吞吐（tokens/s）
  - 并发连接数、缓存命中率
- 成本（Cost）
  - Token 成本（输入/输出）、向量存储、推理资源（GPU/CPU）
  - 单次请求成本（CPT）、单位提升成本（Cost per Gain）
- 风险（Risk）
  - 失败率、超时率、回滚次数、SLA 违约率

