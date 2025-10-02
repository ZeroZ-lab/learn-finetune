# 03｜KV Cache：推理加速与显存估算

目标
- 掌握自回归生成中 KV Cache 的作用与复杂度变化。
- 学会估算 KV Cache 的显存占用。

要点
- 无 Cache：每步注意力与全部前缀计算，复杂度 O(T^2)。
- 有 Cache：缓存历史 K/V，复杂度近似 O(T)。
- 显存估算：B×L×H×S×D×dtype_size×2（K 与 V）。

练习
- 代入 B=2, L=24, H=16, S=1024, D=128, fp16(2B) 估算占用（MB）。
- 思考：超长上下文时如何裁剪/压缩 Cache？

排错
- 生成崩溃常见因：Cache 尺寸配置不当、dtype 不一致、device 不匹配。

