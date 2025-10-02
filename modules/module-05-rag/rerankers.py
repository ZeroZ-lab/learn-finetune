from __future__ import annotations

from typing import List, Tuple


def simple_rerank(query: str, candidates: List[Tuple[str, float, dict, str]], top_k: int = 5):
    """简单重排：按原相似度与长度惩罚组合评分。

    candidates: List of (doc_id, sim, meta, text)
    """
    scored = []
    for doc_id, sim, meta, text in candidates:
        penalty = 0.1 * (len(text) / 1000.0)
        score = sim - penalty
        scored.append((doc_id, score, meta, text))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]

