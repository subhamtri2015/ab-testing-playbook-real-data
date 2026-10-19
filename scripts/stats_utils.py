from __future__ import annotations

import math
from typing import Iterable, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import NormalIndPower


def two_proportion_z_test(a_success: float, a_total: int, b_success: float, b_total: int):
    """Return diff, pooled_z, p_value, ci_low, ci_high, relative_lift."""
    a_prop = a_success / a_total
    b_prop = b_success / b_total
    diff = b_prop - a_prop
    pooled = (a_success + b_success) / (a_total + b_total)
    se_pooled = math.sqrt(pooled * (1 - pooled) * (1 / a_total + 1 / b_total))
    z_stat = diff / se_pooled if se_pooled > 0 else 0.0
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    se_unpooled = math.sqrt(a_prop * (1 - a_prop) / a_total + b_prop * (1 - b_prop) / b_total)
    z_crit = 1.96
    ci_low = diff - z_crit * se_unpooled
    ci_high = diff + z_crit * se_unpooled
    rel_lift = (b_prop - a_prop) / a_prop if a_prop != 0 else np.nan
    return {
        "diff": diff,
        "z_stat": z_stat,
        "p_value": p_value,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "relative_lift": rel_lift,
    }


def proportion_ci(p: float, n: int, z: float = 1.96):
    se = math.sqrt(p * (1 - p) / n)
    return p - z * se, p + z * se


def bootstrap_diff_ci(a: pd.Series, b: pd.Series, reps: int = 2000, seed: int = 42):
    rng = np.random.default_rng(seed)
    diffs = []
    a_vals = a.to_numpy()
    b_vals = b.to_numpy()
    for _ in range(reps):
        a_sample = rng.choice(a_vals, size=len(a_vals), replace=True)
        b_sample = rng.choice(b_vals, size=len(b_vals), replace=True)
        diffs.append(float(b_sample.mean() - a_sample.mean()))
    diffs = np.array(diffs)
    return np.percentile(diffs, 2.5), np.percentile(diffs, 97.5)


def mann_whitney_u(x: pd.Series, y: pd.Series):
    u, p = stats.mannwhitneyu(x, y, alternative="two-sided", method="auto")
    return u, p


def srm_test(observed: Iterable[int], planned: Iterable[float]):
    observed = np.array(list(observed), dtype=float)
    planned = np.array(list(planned), dtype=float)
    if observed.sum() <= 0:
        return np.nan, np.nan
    expected = observed.sum() * planned / planned.sum()
    chi2_stat = np.sum((observed - expected) ** 2 / expected)
    p_value = 1 - stats.chi2.cdf(chi2_stat, df=len(observed) - 1)
    return chi2_stat, p_value


def mde_from_baseline(baseline: float, n_per_arm: int, alpha: float = 0.05, power: float = 0.80, two_sided: bool = True):
    z_alpha = stats.norm.ppf(1 - alpha / 2) if two_sided else stats.norm.ppf(1 - alpha)
    z_beta = stats.norm.ppf(power)
    p1 = baseline
    p2 = p1
    h = 2 * (np.arcsin(np.sqrt(p2)) - np.arcsin(np.sqrt(p1)))
    # For two-proportion proportion test: absolute diff per arm at fixed n
    absolute = (z_alpha + z_beta) * math.sqrt(2 * p1 * (1 - p1) / n_per_arm)
    relative = absolute / p1 if p1 > 0 else np.nan
    return {
        "absolute": absolute,
        "relative": relative,
        "cohens_h": h,
    }


def required_n_for_lift(baseline: float, target_abs_lift: float, alpha: float = 0.05, power: float = 0.80, two_sided: bool = True):
    z_alpha = stats.norm.ppf(1 - alpha / 2) if two_sided else stats.norm.ppf(1 - alpha)
    z_beta = stats.norm.ppf(power)
    if baseline <= 0:
        return np.nan
    n = (z_alpha + z_beta) ** 2 * (2 * baseline * (1 - baseline)) / (target_abs_lift ** 2)
    return n


def holm_adjust(p_values: List[float]):
    p = np.asarray(p_values, dtype=float)
    n = len(p)
    if n == 0:
        return []
    order = np.argsort(p)
    sorted_p = p[order]
    adjusted_sorted = np.empty(n, dtype=float)
    running = 0.0
    for i in range(n):
        rank = n - i
        val = sorted_p[i] * rank
        running = max(running, val)
        adjusted_sorted[i] = min(1.0, running)
    # enforce monotonicity from smallest to largest p-values
    for i in range(1, n):
        adjusted_sorted[i] = max(adjusted_sorted[i], adjusted_sorted[i - 1])
    adjusted = np.empty(n, dtype=float)
    adjusted[order] = adjusted_sorted
    return adjusted.tolist()


def benjamini_hochberg(p_values: List[float], q: float = 0.05):
    p = np.array(p_values, dtype=float)
    n = len(p)
    order = np.argsort(p)
    adjusted = np.empty(n, dtype=float)
    running = 1.0
    for rank, idx in enumerate(reversed(order), start=1):
        pos = n - rank + 1
        adjusted[idx] = min(running, p[idx] * (n / pos))
        running = adjusted[idx]
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    return adjusted.tolist()


def random_effects_meta_analysis(effect_sizes: List[float], variances: List[float]):
    if not effect_sizes:
        return np.nan, np.nan, np.nan, np.nan
    yi = np.asarray(effect_sizes, dtype=float)
    vi = np.asarray(variances, dtype=float)
    wi = 1 / vi
    q = np.sum(wi * (yi - np.average(yi, weights=wi)) ** 2)
    c = np.sum(wi) - np.sum(wi ** 2) / np.sum(wi)
    tau2 = max(0.0, (q - (len(yi) - 1)) / c) if c > 0 else 0.0
    w_star = 1 / (vi + tau2)
    pooled = np.sum(w_star * yi) / np.sum(w_star)
    se = math.sqrt(1 / np.sum(w_star))
    ci_low = pooled - 1.96 * se
    ci_high = pooled + 1.96 * se
    return pooled, se, ci_low, ci_high, tau2


def read_upworthy_tests(path: str):
    df = pd.read_csv(path)
    id_col = next((c for c in df.columns if 'test' in c.lower() and 'id' in c.lower()), None)
    if id_col is None:
        id_col = df.columns[0]
    click_col = next((c for c in df.columns if 'click' in c.lower()), None)
    impr_col = next((c for c in df.columns if 'impr' in c.lower()), None)
    date_col = next((c for c in df.columns if 'date' in c.lower() or 'created' in c.lower()), None)
    headline_col = next((c for c in df.columns if 'head' in c.lower()), None)
    if click_col is None or impr_col is None:
        raise ValueError(f'Need clicks/impressions columns in {path}')
    return df, id_col, click_col, impr_col, date_col, headline_col
