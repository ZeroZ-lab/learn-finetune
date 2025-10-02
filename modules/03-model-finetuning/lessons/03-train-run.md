# 03｜训练脚本运行与监控

目标
- 跑通最小 LoRA 训练脚本并观察 loss 曲线。

步骤
```
python modules/03-model-finetuning/finetune_lora.py \
  --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
  --train-file modules/03-model-finetuning/data/clean.jsonl \
  --output-dir outputs/lora-tinyllama \
  --epochs 1 --batch-size 2 --lr 2e-4
```

观察
- loss 随 epoch 下降且稳定；若震荡剧烈，先降低 lr 或调小 r。

扩展
- 增加验证集与 early stopping；对接 WandB/TensorBoard。
