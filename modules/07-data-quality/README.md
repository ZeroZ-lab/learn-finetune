# 模块 7：数据分析与清洗（CO7）

数据是效果的地基。本模块构建“质量门控→清洗→对齐→证明提升”的闭环，确保模型迭代以数据为先。

学习目标（对齐 CO7）
- 编写可复用的清洗与门控脚本（去重、长度/空值、规则过滤）。
- 使用统计与规则方法识别脏样本，门控拦截率 ≥90%。
- 通过前后对比证明训练/检索指标稳定提升。

目录与示例
- cleaning.py：核心规则（去重/长度/门控）。
- tests/：规则单测，保障质量。
- expectations/：Great Expectations 配置占位。

运行测试
```
pip install pandas pytest
pytest modules/07-data-quality/tests -q
```

1. 数据 Profiling 与基线
- 指标：缺失率、唯一值、长度分布、语言分布、异常值。
- 工具：pandas‑profiling/ydata‑profiling，先“看数据”再设计规则。

2. 清洗规则设计
- 必要字段：instruction/output 非空；input 允许为空。
- 长度范围：10–2048（按业务与模型上下文调整）。
- 去重：精确/模糊（MinHash/SimHash 可选）；保留高质量版本。
- 噪声门控：URL/SQL 注入/脚本片段等高风险模式拦截（示例见 cleaning.py）。

3. 分布对齐与数据增强
- 训练/验证分布一致性：避免数据泄漏与偏置。
- 增强：回译/同义替换/模板化；谨防引入模式化噪声。

4. 质量证明与可追溯
- 对比前后：训练 loss、评测集准确率/偏好、RAG 指标。
- 产出：清洗报告（规则、拦截率、效果证明）与可复现实验脚本。

5. 常见坑位
- 只看整体均值：关注长尾与分布偏移；绘制分布直方图。
- 规则过严：过度过滤导致样本不足；设置灰名单与人工抽检。
- 缺乏版本化：数据版本与规则版本应纳入实验追踪。

学习路径（循序渐进）
- lessons/01-profiling.md：数据 Profiling
- lessons/02-rules.md：清洗规则与门控
- lessons/03-distribution.md：分布对齐与泄漏防护
- lessons/04-enhancement.md：数据增强与风险
- lessons/05-reporting.md：清洗报告与复现
