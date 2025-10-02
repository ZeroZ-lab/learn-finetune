# 模块 1：Python 工程化与 FastAPI 服务端开发（CO6）

本模块聚焦于可上线的服务端工程能力：项目脚手架、SSE 流式接口、鉴权与限流、可观测性（日志/指标/追踪）、基础测试与压测准备。

学习目标（对齐 CO6）
- 搭建工程化项目（`src/` 布局、依赖与代码质量工具）。
- 实现 SSE 流式接口、API Key 鉴权、IP 限流。
- 集成 Prometheus 指标与结构化日志；理解 P99 延迟与 QPS。

快速开始
1) 安装依赖（建议虚拟环境）：
```
pip install fastapi uvicorn prometheus-client
```
2) 运行服务：
```
uvicorn modules.module-01-fastapi.app.main:app --reload
```
3) 验证：
- 健康检查：`curl http://127.0.0.1:8000/health`
- SSE 流式：`curl -N http://127.0.0.1:8000/chat`
- 指标：`curl http://127.0.0.1:8000/metrics`

可选：开启鉴权
```
export API_KEY=secret-key
curl -H "x-api-key: secret-key" http://127.0.0.1:8000/health
```

—

学习路径（循序渐进）
- lessons/01-setup.md：工程化项目脚手架
- lessons/02-sse.md：SSE 流式接口
- lessons/03-auth-rate-limit.md：鉴权与限流
- lessons/04-observability.md：日志与指标
- lessons/05-testing-benchmark.md：测试与压测

—

1. 项目工程化要点
- 结构：将应用代码放在 `app/`，测试放在 `tests/`，便于隔离依赖与快速定位。
- 依赖管理：建议用 uv/Poetry 固定版本与锁文件，保证复现实验环境。
- 质量工具：
  - Ruff：Linter + Formatter；统一风格、减少审阅成本。
  - MyPy：静态类型检查，尽早暴露潜在类型错误。

2. FastAPI 与 ASGI 生态
 - FastAPI 构建于 Starlette 与 Pydantic：
  - 自动生成 Swagger 文档与数据校验。
  - 依赖注入（DI）使业务逻辑与基础设施（DB/缓存）解耦。
- ASGI 服务器：uvicorn/hypercorn；生产可配合 gunicorn 多进程。

提示：本示例将 Prometheus 依赖声明为可选，未安装时会以回退占位运行（/metrics 返回 501），便于快速体验。

3. SSE（Server‑Sent Events）实现与实践
- SSE 适合单向流式输出（Chat/生成中间结果/日志）；浏览器与 curl 都易于消费。
- 关键实现点：Content‑Type `text/event-stream`，分块发送 `data: <json>\n\n`。
- 示例：`/chat` 端点逐 token 发送 JSON；最后发送 `done: true`。

4. 鉴权与限流
- API Key：在 Header（如 `x-api-key`）中传递；服务端从环境变量加载期望值。
- 限流策略：
  - 简易实现：滑动时间窗口计数（示例：60s 内最多 10 次）。
  - 生产建议：令牌桶/漏桶 + Redis/网关级限流（Nginx/Envoy/Kong）。

5. 可观测性（Observability）
- 指标：Prometheus Counter/Summary/Histogram；关键指标如 QPS、延迟分位（P95/P99）。
- 日志：结构化（JSON）便于集中检索与关联；记录 trace_id/span_id。
- 追踪：OpenTelemetry 采集；与应用指标在同一面板中联动排障。

6. 测试与压测
- 单测：使用 TestClient（见 `tests/test_app.py`）校验健康检查与 SSE 收尾标志。
- 压测准备：wrk/hey/locust；对 `/chat` 与核心 API 做 QPS、P95/P99 观察。
- 基线目标：本机 QPS ≥30，错误率 <1%。

7. 常见坑位
- SSE 输出缓冲：需禁用中间代理的缓冲；及时 flush 输出。
- 多进程与全局状态：限流/计数器使用进程外存储（Redis）避免不一致。
- 健康检查与就绪检查：区分 `/health` 与 `/ready`，配合部署平台探针。

8. 延伸阅读
- FastAPI 官方文档；Prometheus 指南；OpenTelemetry 入门。
