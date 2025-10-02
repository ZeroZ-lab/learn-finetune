# 评测数据集示例

- `eval_sample.jsonl`：3 条示例指令，用于演示 `evaluate_model.py` 的数据格式。
- 字段说明：
  - `prompt`：已经模板化的提示（建议与训练模板保持一致）。
  - `expected`：期望输出，用于 Exact Match。

实践中可将业务评测集整理为同样结构，或在 `evaluate_model.py` 中扩展解析逻辑以适配自定义模板。
