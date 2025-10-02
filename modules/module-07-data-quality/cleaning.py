from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List, Tuple

import pandas as pd


@dataclass
class Rules:
    min_len: int = 10
    max_len: int = 2048
    drop_na: bool = True


def apply_rules(df: pd.DataFrame, rules: Rules) -> pd.DataFrame:
    df2 = df.copy()
    if rules.drop_na:
        df2 = df2.dropna(subset=["instruction", "output"])  # 必要字段
    # 计算合并文本长度
    text = (df2["instruction"].astype(str) + df2["input"].fillna("").astype(str) + df2["output"].astype(str))
    mask = text.str.len().between(rules.min_len, rules.max_len)
    df2 = df2[mask]
    # 去重
    df2 = df2.drop_duplicates(subset=["instruction", "input", "output"], keep="first")
    return df2.reset_index(drop=True)


def quality_gate(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """简单门控：拦截包含明显噪声模式的样本。

    返回：(passed, rejected)
    """
    pattern = re.compile(r"(http[s]?://\S+|<script|select\s+\*|drop\s+table)", re.I)
    text = (df["instruction"].astype(str) + df["input"].fillna("").astype(str) + df["output"].astype(str))
    bad = text.str.contains(pattern)
    return df[~bad].reset_index(drop=True), df[bad].reset_index(drop=True)

