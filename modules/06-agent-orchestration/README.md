# 模块 6：Agent 编排（纯 Python 状态机）（CO5）

本模块拆解 Agent 的核心：感知‑决策‑执行‑记忆‑回放。通过最小状态机理解 ReAct 与 Plan‑Execute 的差异与组合方式，并实现可回放与容错的多工具编排。

学习目标（对齐 CO5）
- 设计「工具规范 + 决策器 + 记忆 + 容错 + 回放」的最小闭环。
- 实现多工具调用、超时/重试/降级，端到端成功率 ≥85%。
- 产出可回放日志，支持故障注入与复盘。

目录与示例
- agent.py：简单 Orchestrator（启发式决策）。
- tools/：`calculator.py`（算术）、`retrieval_stub.py`（检索占位）。
- replay_logger.py：JSON Lines 回放日志。

快速运行
```
python modules/06-agent-orchestration/agent.py --query "计算 3*(4+5) 并给出结果"
```

1. 范式对比
- ReAct：边思考边行动，易于溯源；但可能反复试错导致时延增长。
- Plan‑Execute：先规划后执行，层次化拆解任务；对复杂任务更稳，但规划质量依赖模型。
- 实践：两者混合，设置最大步数与降级路径。

2. 关键组件
- 工具（Tool）：定义 Function Schema（名称、参数、返回）；参数校验与异常语义。
- 决策器（Policy）：启发式/学习策略/LLM 选择工具与输入。
- 记忆（Memory）：短期（对话/步骤）、长期（知识库/向量）；压缩与检索策略。
- 容错：超时、重试（指数退避）、回退（换工具/降级）、熔断。
- 回放：记录每一步的输入/输出/耗时/异常，用于 Debug 与评估。

3. 评估指标
- 成功率：端到端达到目标的比例。
- 工具失败率与超时率：聚焦瓶颈工具优化。
- 平均步数与时延：在成功率不降的前提下优化速度。

4. 常见坑位
- 工具接口脆弱：引入参数校验与默认值；降级策略要明确。
- 决策循环：上限步数 + 内容去重（防止在同一状态反复）。
- 过度依赖单一工具：提供等价备选路径以提高鲁棒性。

5. 延伸
- 引入 LLM 作为决策器；用 JSON 模式约束工具调用参数。
- 任务图（Task Graph）与并行执行；回放到可视化界面（前端/Notebook）。

学习路径（循序渐进）
- lessons/01-paradigms.md：ReAct 与 Plan‑Execute
- lessons/02-tools-schema.md：工具规范与参数校验
- lessons/03-policy.md：决策器与停机条件
- lessons/04-memory.md：记忆与压缩
- lessons/05-reliability.md：可靠性策略
- lessons/06-replay.md：回放与可观测
