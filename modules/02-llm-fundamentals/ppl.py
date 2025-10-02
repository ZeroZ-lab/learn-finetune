"""Perplexity (PPL) computation utilities.

If you already have token-level negative log-likelihoods (NLL),
PPL = exp(mean(NLL)). For demonstration, we also provide a simple
cross-entropy over logits and target indices using NumPy.
"""
from __future__ import annotations

import numpy as np


def log_softmax(x: np.ndarray) -> np.ndarray:
    x = x - np.max(x, axis=-1, keepdims=True)
    logsumexp = np.log(np.sum(np.exp(x), axis=-1, keepdims=True))
    return x - logsumexp


def ppl_from_nll(nlls: np.ndarray) -> float:
    nlls = np.asarray(nlls, dtype=np.float64)
    return float(np.exp(np.mean(nlls)))


def sequence_nll(logits: np.ndarray, targets: np.ndarray) -> float:
    """Compute mean negative log-likelihood for a sequence.

    Args:
        logits: shape [T, V]
        targets: shape [T], token indices in [0, V)
    """
    if logits.ndim != 2:
        raise ValueError("logits must be [T,V]")
    if targets.ndim != 1 or targets.shape[0] != logits.shape[0]:
        raise ValueError("targets must be [T] and match logits T")
    ls = log_softmax(logits)
    row_idx = np.arange(targets.shape[0])
    selected = ls[row_idx, targets]
    nll = -np.mean(selected)
    return float(nll)


def ppl_from_logits(logits: np.ndarray, targets: np.ndarray) -> float:
    return float(np.exp(sequence_nll(logits, targets)))


__all__ = ["ppl_from_nll", "sequence_nll", "ppl_from_logits"]

