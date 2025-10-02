# 05｜困惑度（PPL）：语言建模指标的理解

目标
- 掌握 PPL 与 NLL/交叉熵的关系，理解其意义与局限性。

概念
- PPL = exp(mean(NLL))，越低表示模型对真实样本越不惊讶。
- 注意：PPL 不是任务效果的直接度量（如信息抽取的 F1）。

步骤
1) 阅读 `ppl.py` 的 `sequence_nll` 与 `ppl_from_logits`。
2) 自造简单 logits 与 targets，验证 `ppl ≈ exp(nll)`。
3) 设计两组 logits（“好”与“差”），对比 PPL。

扩展
- 将 PPL 与任务指标（准确率/偏好）一起报告，避免单指标误导。

