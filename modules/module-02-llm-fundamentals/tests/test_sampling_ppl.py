import importlib.util
from pathlib import Path
import numpy as np

BASE = Path(__file__).resolve().parents[1]

def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, str(BASE / file))
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    assert spec and spec.loader
    spec.loader.exec_module(mod)  # type: ignore
    return mod

sampling = _load("sampling", "sampling.py")
ppl = _load("ppl", "ppl.py")


def test_sample_top_p_returns_index():
    logits = np.array([0.0, 1.0, 2.0, -1.0])
    idx = sampling.sample_top_p(logits, temperature=0.8, top_p=0.9, rng=np.random.default_rng(0))
    assert isinstance(idx, int)
    assert 0 <= idx < logits.shape[0]


def test_ppl_from_nll():
    nlls = np.array([1.0, 2.0, 3.0])
    v = ppl.ppl_from_nll(nlls)
    assert v > 0


def test_ppl_from_logits_matches_sequence_nll():
    logits = np.array([[2.0, 0.0], [0.0, 2.0]])  # prefer 0 then 1
    targets = np.array([0, 1])
    nll = ppl.sequence_nll(logits, targets)
    v = ppl.ppl_from_logits(logits, targets)
    assert np.isclose(v, np.exp(nll))
