"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    tp = sum(h == POS and j == POS for h, j in zip(human, judge))
    fp = sum(h != POS and j == POS for h, j in zip(human, judge))
    fn = sum(h == POS and j != POS for h, j in zip(human, judge))
    tn = sum(h != POS and j != POS for h, j in zip(human, judge))
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    cm = confusion(human, judge)
    p = cm["tp"] / (cm["tp"] + cm["fp"]) if (cm["tp"] + cm["fp"]) else 0.0
    r = cm["tp"] / (cm["tp"] + cm["fn"]) if (cm["tp"] + cm["fn"]) else 0.0
    return float(p), float(r)


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """kappa = (p_o - p_e) / (1 - p_e). Raise ValueError when undefined (p_e == 1):
    a constant judge has no signal and must FAIL calibration, not pass on a technicality."""
    n = len(human)
    if n == 0:
        raise ValueError("empty input")
    cm = confusion(human, judge)
    p_o = (cm["tp"] + cm["tn"]) / n
    judge_pos = (cm["tp"] + cm["fp"]) / n
    judge_neg = (cm["tn"] + cm["fn"]) / n
    human_pos = (cm["tp"] + cm["fn"]) / n
    human_neg = (cm["tn"] + cm["fp"]) / n
    p_e = judge_pos * human_pos + judge_neg * human_neg
    if abs(1.0 - p_e) < 1e-12:
        raise ValueError("p_e == 1: kappa undefined for constant agreement")
    return float((p_o - p_e) / (1.0 - p_e))


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct an observed failure rate for judge error; clip to [0, 1]."""
    denom = sensitivity + specificity - 1.0
    if abs(denom) < 1e-12:
        return 0.0
    corrected = (observed_rate + specificity - 1.0) / denom
    return float(max(0.0, min(1.0, corrected)))


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy.stats import bootstrap

    if len(a) != len(b):
        raise ValueError("sequences must be same length")
    if all(abs(x - y) <= 1e-12 for x, y in zip(a, b)):
        return (0.0, 0.0, 0.0)

    d = float(np.mean(a) - np.mean(b))
    res = bootstrap(
        (np.array(a), np.array(b)),
        statistic=lambda x, y: np.mean(x) - np.mean(y),
        paired=True,
        n_resamples=n_resamples,
        random_state=np.random.default_rng(rng),
        confidence_level=confidence,
        method="percentile",
    )
    return (d, float(res.confidence_interval.low), float(res.confidence_interval.high))


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    import math

    if k > n or k <= 0 or n <= 0 or c < 0 or c > n:
        raise ValueError(f"invalid args: n={n}, c={c}, k={k}")
    if n - c < k:
        return 1.0
    return float(1.0 - math.comb(n - c, k) / math.comb(n, k))


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    import math

    if k > n or k <= 0 or n <= 0 or c < 0 or c > n:
        raise ValueError(f"invalid args: n={n}, c={c}, k={k}")
    if c < k:
        return 0.0
    return float(math.comb(c, k) / math.comb(n, k))
