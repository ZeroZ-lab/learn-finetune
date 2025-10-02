# 模块化课程资源总览（modules/）

本目录按“最终大纲 v2.1”的 8 个模块进行组织。每个模块包含：
- README：学习目标（对应 COx）、内容要点、运行指南
- labs/：动手实验说明与提交要求
- examples/ 或 app/：可运行的最小代码示例（展示工程能力）
- tests/：关键功能的轻量级单元测试（如适用）

新增：每个模块提供 lessons/ 按序号递进的学习文档（01-..）。建议按 lessons 顺序学习，再回到 README 汇总与扩展练习。

目录：
- 01-fastapi-service/ —— FastAPI 工程化与可观测（CO6）
- 02-llm-fundamentals/ —— LLM 原理与推理优化（CO1）
- 03-model-finetuning/ —— SFT/LoRA/QLoRA 微调（CO2）
- 04-prompt-engineering/ —— Prompt 系统化方法（CO3）
- 05-rag-system/ —— RAG 全链路（Milvus/本地回退）（CO4）
- 06-agent-orchestration/ —— 多工具 Agent 编排（CO5）
- 07-data-quality/ —— 数据清洗与质量门控（CO7）
- 08-business-ops/ —— 业务闭环与灰度/成本（CO8）

提示：示例代码尽量无外部依赖或提供“回退实现”。如需完整能力（如 Milvus、Transformers 微调），请根据各模块 README 安装相应依赖。
