# 04｜离线评估与 A/B 实验

目标
- 建立离线评估集，完成 A/B 模板对比并统计显著性。

步骤
- 准备 `eval/testset.jsonl`；运行 `evaluate_prompts.py` 获取 acc_a/acc_b。
- 分析 delta 与样本量是否足够；如可行，扩大样本验证稳定性。

扩展
- 结合模块 8 的显著性与功效分析，设定提前停止与止损策略。

