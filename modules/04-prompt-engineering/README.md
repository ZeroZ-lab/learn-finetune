# 模块 4：Prompt Engineering 系统化方法（CO3）

本模块梳理 Prompt 的系统化方法论：从角色设定到结构化输出与自动化评估，形成可迁移的最佳实践与基线。

学习目标（对齐 CO3）
- 能设计 System Prompt、Few‑Shot、CoT/ReAct 模式并解释适用场景。
- 能使用 JSON Schema + Pydantic 进行结构化输出与结果校验。
- 能完成离线评估与 A/B 实验设计，达成 ≥15% 的效果提升。

目录与示例
- templates/：两套分类模板（A 基准、B 优化）。
- eval/evaluate_prompts.py：离线评估脚本（可对接在线/本地模型，提供 dummy provider 演示）。
- eval/testset.jsonl：样本测试集。

快速运行
```
pip install pydantic
python modules/04-prompt-engineering/eval/evaluate_prompts.py --provider dummy \
  --template-a modules/04-prompt-engineering/templates/classification_base.md \
  --template-b modules/04-prompt-engineering/templates/classification_optimized.md \
  --testset modules/04-prompt-engineering/eval/testset.jsonl
```

1. Prompt 模式与范式
- System Prompt：定义角色、风格、约束；确保稳定可控。
- Few‑Shot：用示例引导格式与推理模式；样例选择策略（难例/代表性例）。
- CoT：显式「逐步思考」；在可解释性与时延之间权衡。
- ReAct：Reasoning + Acting；配合工具调用（见模块 6）。

2. 结构化输出与校验
- 输出 JSON：格式严格与边界条件（空值/非法值/溢出）。
- JSON Schema + Pydantic：在服务端做结构化校验并返回清晰错误。

3. 评估与 A/B
- 指标：准确率/宏平均 F1/编辑距离/业务自定义得分。
- LLM‑as‑Judge 的风险与缓解：
  - 避免与被评模同源；加入对抗样例与多裁判平均。
  - 留出人工抽检样本校准。
- 统计显著性：最小样本量估计、置信区间、功效分析（参见模块 8）。

4. 常见问题
- 提示漂移：对关键字段使用示例锁定格式；失败时回退到更保守的模板。
- 多语言处理：对语言敏感任务，明确指定语言与编码；必要时翻译预处理。
- 上下文过长：裁剪/摘要/检索；使用占位符缩小模板体积。

5. 参考资料
- Prompt Engineering Guide
- ReAct / Chain‑of‑Thought 论文与社区资源

学习路径（循序渐进）
- lessons/01-system-prompt.md：System Prompt 与任务定义
- lessons/02-few-shot.md：Few‑Shot 与示例选择
- lessons/03-structured-output.md：结构化输出与校验
- lessons/04-ab-testing.md：离线评估与 A/B
- lessons/05-llm-as-judge.md：LLM‑as‑Judge
