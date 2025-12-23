from __future__ import annotations
import numpy as np
from scipy.signal import butter, filtfilt

def design_lowpass(fs: float, cutoff_hz: float, order: int = 10) -> tuple[np.ndarray, np.ndarray]:
    """
    Design a low-pass Butterworth filter.
    """
    nyq = fs / 2.0
    wn = cutoff_hz / nyq
    b, a = butter(order, wn, btype="low")
    return b, a

def apply_filtfilt(trials: np.ndarray, b: np.ndarray, a: np.ndarray) -> np.ndarray:
    """
    Apply zero-phase filtering along time axis.
    trials: (num_trials, num_samples)
    """
    return filtfilt(b, a, trials, axis=1)
