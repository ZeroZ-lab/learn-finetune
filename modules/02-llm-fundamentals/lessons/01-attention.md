# 01｜Self‑Attention 与 Multi‑Head 直觉与实现

目标
- 讲清 Q/K/V 与注意力权重的含义与计算流程。
- 理解 Multi‑Head 的动机与优势。

核心概念
- 线性投影：Q= XW_Q，K= XW_K，V= XW_V。
- 注意力：softmax(QK^T/√d_k)·V，实现「对齐」相关信息。
- Multi‑Head：将 d 拆分为多头并行注意力，提升表达能力。

推导要点
1) 标准化缩放：除以 √d_k 避免点积值过大导致梯度不稳。
2) 残差 + 层归一化：稳定训练，便于加深网络。
3) FFN：两层线性 + 非线性（GELU/ReLU）提升特征表达。

动手练习（思考题）
- 给定 X∈R^{T×d} 与投影矩阵，手算一个 T=2, d=4 的最小例，验证 softmax 权重之和为 1。

延伸阅读
- Attention Is All You Need（Vaswani et al., 2017）

