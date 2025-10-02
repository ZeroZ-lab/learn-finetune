# 04｜可观测性：日志与指标

目标
- 集成 Prometheus 指标与结构化日志，理解 QPS 与延迟分位。

步骤
1) 安装：`pip install prometheus-client`。
2) 访问 `/metrics`，确认基础指标输出；未安装依赖时返回 501（回退）。
3) 添加 `Counter`/`Summary`/`Histogram` 观测关键路径。

扩展
- 引入 OpenTelemetry 追踪，关联日志与指标进行端到端排障。

