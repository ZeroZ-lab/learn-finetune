# 模块 3：小模型微调（SFT/LoRA/QLoRA）（CO2）

本模块从数据→微调→评测→量化部署的全链路出发，使用 Transformers + PEFT 实现高性价比的小模型指令微调，并确保可复现。

学习目标（对齐 CO2）
- 清洗与模板化指令数据（JSONL），建立最小可复现数据管线。
- 用 LoRA/QLoRA 完成 SFT 微调，达到评测集效果 ≥ 基座 +10%。
- 完成 int4 量化并在本地（Apple Silicon/CPU）推理。

环境准备
```
pip install transformers peft datasets accelerate bitsandbytes
```

1. 数据规范与清洗
- JSONL 格式（建议）：{"instruction", "input", "output"}
- 质量门控：长度、语言、重复、毒性/违法内容过滤（详见模块 7）。
- 运行示例：
```
python prepare_data.py --input raw.jsonl --output data/clean.jsonl --min-len 10 --max-len 2048
```

2. LoRA/QLoRA 原理速览
- LoRA：在部分矩阵上引入低秩分解 A·B（秩 r≪d），仅训练 A/B；节省显存与训练时间。
- QLoRA：通过 nf4/4bit quantization 将权重量化，叠加 LoRA 训练；进一步降低资源占用。
- 超参提示：r/alpha/dropout 与学习率存在耦合，建议网格/贝叶斯小范围搜索。

3. 训练脚本与运行
```
python finetune_lora.py \
  --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
  --train-file data/clean.jsonl \
  --output-dir outputs/lora-tinyllama \
  --epochs 1 --batch-size 2 --lr 2e-4
```
- 说明：脚本使用 Trainer + DataCollatorForLanguageModeling，示范性为主。生产需要加入验证、早停、lr schedule、混合精度与日志平台（W&B）。

4. 评测与对比
- 构建小型评测集：分类/抽取/问答，避免训练泄漏。
- 度量：准确率/偏好（pairwise）/PPL；对比基座与 LoRA 模型，目标 ≥ +10%。

5. 量化与部署
- int4：bitsandbytes 或 MLX（Apple Silicon）进行推理量化；注意量化误差对指标的影响。
- 部署：结合模块 1 的 FastAPI，提供 `/generate` 接口，观测延迟与 QPS。

6. 常见坑位
- 数据「模板不一致」导致学习困难：统一 special tokens 与对话模板。
- 学习率过大/过小：观测 loss 曲线是否稳定下降；必要时降低 batch size 并启用梯度累积。
- 显存不足：缩短 max_length 或采用 QLoRA；考虑 CPU/MPS 训练小模型。

7. 参考资料
- LoRA: Low‑Rank Adaptation of Large Language Models
- QLoRA: Efficient Finetuning of Quantized LLMs

学习路径（循序渐进）
- lessons/01-data-cleaning.md：数据清洗与模板化
- lessons/02-lora-theory.md：LoRA/QLoRA 原理
- lessons/03-train-run.md：训练脚本运行与监控
- lessons/04-eval.md：评测与对比
- lessons/05-quantization.md：量化与本地推理
