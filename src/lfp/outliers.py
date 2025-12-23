from __future__ import annotations
import numpy as np

def baseline_outlier_mask(raw_trials: np.ndarray, baseline_end: int, k: float = 5.0) -> tuple[np.ndarray, dict]:
    """
    Baseline-based outlier rejection using robust stats (median + k*MAD) on baseline std.

    Parameters
    ----------
    raw_trials : (num_trials, num_samples)
    baseline_end : int
        Samples [0:baseline_end] are treated as baseline (pre-stimulus).
    k : float
        Threshold multiplier for MAD.

    Returns
    -------
    keep_mask : (num_trials,) bool
        True if the trial is kept.
    info : dict
        Contains threshold, median, mad, baseline_std, n_before, n_after.
    """
    baseline = raw_trials[:, :baseline_end]
    baseline_std = baseline.std(axis=1)

    med = np.median(baseline_std)
    mad = np.median(np.abs(baseline_std - med))

    if mad == 0:
        thr = med * 1.5
    else:
        thr = med + k * mad

    keep_mask = baseline_std <= thr
    info = {
        "median": float(med),
        "mad": float(mad),
        "threshold": float(thr),
        "n_before": int(raw_trials.shape[0]),
        "n_after": int(keep_mask.sum()),
    }
    return keep_mask, info

def tone_indices(tone_info: np.ndarray) -> tuple[np.ndarray, np.ndarray, float, float]:
    """
    Return low/high tone trial indices and their tone values.
    """
    t = tone_info.squeeze()
    vals = np.unique(t)
    low_val, high_val = float(vals.min()), float(vals.max())
    low_idx = np.where(t == low_val)[0]
    high_idx = np.where(t == high_val)[0]
    return low_idx, high_idx, low_val, high_val
