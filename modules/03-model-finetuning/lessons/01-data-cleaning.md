# 01｜数据清洗与模板化

目标
- 将原始指令样本清洗为统一 JSONL 模板：{"instruction","input","output"}。

步骤
1) 明确长度与语言规则；去重策略（精确/模糊）。
2) 运行：
```
python modules/03-model-finetuning/prepare_data.py --input raw.jsonl --output modules/03-model-finetuning/data/clean.jsonl --min-len 10 --max-len 2048
```
3) 人工抽检 20 条，确认模板一致与标签无误。

扩展
- 引入质量门控（见模块 7）拦截噪声样本。
