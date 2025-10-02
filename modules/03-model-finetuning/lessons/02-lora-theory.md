# 02｜LoRA/QLoRA 原理与超参

目标
- 理解 LoRA 的低秩分解思想与可训练参数缩减；掌握 QLoRA 思路。

要点
- LoRA：ΔW ≈ A·B，rank r≪d；仅训练 A、B；前/后向便宜。
- QLoRA：权重量化（nf4/4bit）+ LoRA 训练，显著降显存。
- 超参关联：r、alpha、dropout 与学习率、batch size 耦合。

练习
- 估算同等设置下全量微调 vs LoRA 的可训练参数量差异。

