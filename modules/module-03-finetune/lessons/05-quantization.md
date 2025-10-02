# 05｜量化与本地推理

目标
- 使用 int4 量化降低推理成本；在 CPU/MPS 上运行演示。

要点
- PTQ（后量化）vs QAT（量化感知训练）的权衡。
- MLX（Apple Silicon）与 bitsandbytes（NVIDIA/CPU）生态差异。

实践
- 按目标平台选择工具链，记录延迟、显存/内存占用与效果差异。

