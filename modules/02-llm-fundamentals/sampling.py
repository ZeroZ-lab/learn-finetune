"""Top-p (nucleus) sampling implementation using NumPy.

Reference: Holtzman et al., The Curious Case of Neural Text Degeneration (2020)
"""
from __future__ import annotations

import numpy as np


def softmax(x: np.ndarray) -> np.ndarray:
    x = x - np.max(x)
    e = np.exp(x)
    return e / np.sum(e)


def sample_top_p(
    logits: np.ndarray,
    temperature: float = 1.0,
    top_p: float = 0.9,
    rng: np.random.Generator | None = None,
) -> int:
    """Sample an index from logits with Temperature + Top-p.

    Args:
        logits: shape [V], unnormalized log-probabilities.
        temperature: >0; values <1 sharpen, >1 smooth.
        top_p: cumulative probability threshold in (0,1].
        rng: optional np.random.Generator for reproducibility.

    Returns:
        int: sampled token index.
    """
    if rng is None:
        rng = np.random.default_rng()

    if temperature <= 0:
        raise ValueError("temperature must be > 0")
    if not (0 < top_p <= 1):
        raise ValueError("top_p must be in (0,1]")

    scaled = logits / temperature
    probs = softmax(scaled)
    # sort by prob desc
    idx = np.argsort(-probs)
    sorted_p = probs[idx]
    cum = np.cumsum(sorted_p)
    k = int(np.searchsorted(cum, top_p, side="left")) + 1
    idx_top = idx[:k]
    p_top = sorted_p[:k]
    p_top = p_top / p_top.sum()
    choice = rng.choice(len(idx_top), p=p_top)
    return int(idx_top[choice])


__all__ = ["sample_top_p"]

