import importlib.util
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cleaning", str(BASE / "cleaning.py"))
mod = importlib.util.module_from_spec(spec)  # type: ignore
assert spec and spec.loader
spec.loader.exec_module(mod)  # type: ignore
Rules = mod.Rules
apply_rules = mod.apply_rules
quality_gate = mod.quality_gate


def test_apply_rules_length_and_dedup():
    df = pd.DataFrame([
        {"instruction": "a" * 5, "input": "", "output": "x" * 5},  # too short
        {"instruction": "hello", "input": "world", "output": "!" * 20},  # ok
        {"instruction": "hello", "input": "world", "output": "!" * 20},  # dup
    ])
    out = apply_rules(df, Rules(min_len=10, max_len=100))
    assert len(out) == 1


def test_quality_gate():
    df = pd.DataFrame([
        {"instruction": "正常问题", "input": "", "output": "回答"},
        {"instruction": "看看 http://spam.com", "input": "", "output": "垃圾"},
    ])
    passed, rejected = quality_gate(df)
    assert len(passed) == 1 and len(rejected) == 1
