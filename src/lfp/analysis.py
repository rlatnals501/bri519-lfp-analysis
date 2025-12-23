from __future__ import annotations
import numpy as np
from scipy.signal import welch

def compute_mean_lfp(trials: np.ndarray) -> np.ndarray:
    """
    Mean across trials.
    trials: (num_trials, num_samples)
    """
    return trials.mean(axis=0)

def compute_psd_welch(x: np.ndarray, fs: float, nperseg: int = 256) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute PSD using Welch's method.
    x: (num_samples,)
    """
    f, pxx = welch(x, fs=fs, nperseg=nperseg)
    return f, pxx
