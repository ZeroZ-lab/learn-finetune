# 03｜结构化输出与校验

目标
- 通过 JSON Schema + Pydantic 强约束输出，减少解析错误。

步骤
- 在模板中明确输出 JSON 结构与取值范围。
- 服务端用 Pydantic 验证字段与类型，返回清晰错误信息与纠偏策略。

实践
- 修改 `classification_optimized.md` 的 JSON 输出；在评估脚本中解析与校验。

