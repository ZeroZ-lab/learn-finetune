# 04｜采样策略：Temperature/Top‑k/Top‑p 实战

目标
- 理解温度与截断策略如何影响输出多样性与稳定性。
- 亲手实现并调参 Top‑p 采样。

步骤
1) 阅读 `sampling.py` 的 `sample_top_p` 实现。
2) 修改参数（temperature/top_p），观察选择分布变化。
3) 思考：当 top_p→1 与 temperature→0 时分别对应什么极端情况？

验证
```
pytest modules/module-02-llm-fundamentals/tests -q
```

扩展
- 实现 Top‑k 版本并与 Top‑p 对比在长尾分布下的差异。

