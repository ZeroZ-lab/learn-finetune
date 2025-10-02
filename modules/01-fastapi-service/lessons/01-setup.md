# 01｜工程化项目脚手架与依赖

目标
- 建立最小可维护的 Python 项目结构与依赖管理。

步骤
1) 目录：`app/` 放业务代码，`tests/` 放测试，`README.md` 说明运行与验收。
2) 依赖：建议使用 `uv` 或 `Poetry` 锁定版本；本示例直接用 `pip` 以降低门槛。
3) 质量：引入 Ruff/MyPy（可选），统一格式、提前暴露类型问题。

完成标志
- `python modules/01-fastapi-service/app/server.py` 可启动。
