# 模块 2：LLM 基础原理与推理优化（CO1）

本模块从「概念 → 数学直觉 → 工程实现 → 指标与优化」四个层面，系统讲解 Transformer 与推理优化方法，并配套可运行代码与单测，确保知其然亦知其所以然。

学习目标（对齐 CO1）
- 能清晰讲解 Self‑Attention、Multi‑Head、RoPE、KV Cache 的工作原理与工程取舍。
- 能实现 Temperature + Top‑p 采样；理解其对输出多样性与稳定性的影响。
- 能计算困惑度（PPL），并解释其与交叉熵、模型好坏的关系。

配套代码
- sampling.py：Top‑p（nucleus）采样实现（NumPy）。
- ppl.py：困惑度（PPL）与序列 NLL 计算（NumPy）。
- tests/：基础正确性测试用例。

快速开始
```
pip install numpy pytest
pytest modules/02-llm-fundamentals/tests -q
```

—

学习路径（循序渐进）
- lessons/01-attention.md：Self‑Attention 与 Multi‑Head
- lessons/02-rope.md：RoPE 与长上下文
- lessons/03-kv-cache.md：KV Cache 与显存估算
- lessons/04-sampling.md：采样策略实战
- lessons/05-ppl.md：困惑度与指标理解

1. Transformer 与 Self‑Attention（直觉与数学）
- 目标：以最小符号量解释注意力为何能「对齐」相关信息。
- 记号：输入序列 X∈R^{T×d}。
  - 线性投影得到 Q= XW_Q, K= XW_K, V= XW_V。
  - 注意力权重 α = softmax(QK^T/√d_k)，输出 Y = αV。
- 关键点：
  - Multi‑Head 将 d_k 分组并行，提升表达能力；拼接后再线性整合。
  - 残差与层归一化稳定训练；前馈网络（FFN）做特征非线性映射。

2. 位置编码与 RoPE（旋转位置编码）
- 绝对位置编码：固定或可学习位置向量加到输入上。
- RoPE：将位置编码融入 Q/K 的相位旋转，保持相对位置信息；理论上利于外推与长序列。
- 工程意义：RoPE 兼顾相对位置的平移不变性，在长上下文中表现更稳健。

3. KV Cache 与推理复杂度
- 自回归生成的瓶颈：每步都要重复计算前缀注意力。
- KV Cache：缓存历史 Key/Value，下一步只需与新 Token 的 Query 做点积，复杂度从 O(T^2) 降到 O(T)。
- 显存估算：KV Cache 约占 batch×layers×heads×seq_len×head_dim×dtype_size×2。
  - 例：B=1, L=32, H=32, S=2048, D=128, fp16(2B) → 1×32×32×2048×128×2×2 ≈ 536MB。

4. 采样策略（Temperature/Top‑k/Top‑p）
- Temperature：对 logits 除以 τ；τ<1 更保守，τ>1 更发散。
- Top‑k：截断到概率最高的 k 个候选。
- Top‑p（nucleus）：按累计概率阈值 p 截断，更自适应；本模块实现见 sampling.py。
- 实践建议：
  - 知识问答/工具调用：τ≈0.7–0.9，p≈0.8–0.95。
  - 创意写作：更高 τ 与 p。

5. 困惑度（Perplexity, PPL）
- 定义：PPL = exp(平均 NLL)。越低越好。
- 直觉：模型对真实序列越「不惊讶」，困惑度越低。
- ppl.py 提供两种计算方式：
  - 已知 token‑level NLL → ppl_from_nll()
  - 已知 logits 与标签 → sequence_nll() → ppl_from_logits()

6. 实操步骤
- 运行单测验证实现：
  - Top‑p 采样能返回合法索引。
  - PPL 与 NLL 的关系满足 ppl ≈ exp(nll)。
- 调参小实验（建议自己再做）：
  - 固定 logits，改变 τ 与 p，观察采样分布与多样性变化。
  - 构造两组 logits（好/差），对比 PPL。

7. 性能与优化要点
- Flash Attention：通过重写注意力计算减少显存峰值并加速；需要框架与硬件支持。
- Continuous Batching：服务端层面的动态批处理，提高吞吐（tokens/s）。
- KV Cache 管理：
  - 分配策略：静态/动态分配；回收与复用。
  - 长上下文：滑动窗口、稀疏注意力、分块解码。

8. 常见坑位与排查
- 采样导致输出「漂移」：τ/p 过大；限制最大生成长度和重复惩罚。
- PPL 与实际业务指标不一致：PPL 是语言建模指标，不等同于任务表现；需结合任务评估（如准确率、Faithfulness）。
- 长序列爆显存：确认 KV Cache 形状与 dtype；必要时量化或裁剪上下文。

9. 参考资料
- Attention Is All You Need（Vaswani et al., 2017）
- The Curious Case of Neural Text Degeneration（Holtzman et al., 2020）
- RoFormer/RoPE 相关论文与实现说明
