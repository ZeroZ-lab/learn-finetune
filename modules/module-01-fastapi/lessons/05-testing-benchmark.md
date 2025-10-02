# 05｜测试与压测

目标
- 使用 TestClient 编写基本单元测试；准备 wrk/hey/locust 压测。

步骤
1) 运行单测：`pytest modules/module-01-fastapi/tests -q`。
2) 压测：`wrk -t4 -c64 -d30s http://127.0.0.1:8000/health`；记录 QPS 与 P99。
3) 观察 `/metrics` 中的请求计数与延迟，确认无明显错误。

验收
- 本机 QPS ≥30；错误率 <1%。

