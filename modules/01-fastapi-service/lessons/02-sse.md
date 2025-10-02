# 02｜SSE 流式接口实现

目标
- 实现 `text/event-stream` 的 SSE 接口，逐步推送生成内容。

步骤
1) 阅读 `app/server.py` 的 `/chat`，理解 `StreamingResponse` 与生成器。
2) 确认每条消息格式：`data: {json}`，以空行分割；最后发送 `done: true`。
3) 使用 `curl -N` 验证逐行输出。

扩展
- 添加 `id` 递增实现断点续传（可选）。
