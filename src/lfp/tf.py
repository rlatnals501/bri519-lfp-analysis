from __future__ import annotations
import numpy as np
from scipy.signal import spectrogram

def compute_spectrogram(
    x: np.ndarray,
    fs: float,
    window: np.ndarray,
    noverlap: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Spectrogram for a 1D signal x.
    Returns (f, t, Sxx)
    """
    f, t, Sxx = spectrogram(
        x, fs=fs, window=window, noverlap=noverlap, nfft=None,
        nperseg=len(window), scaling="density", mode="psd"
    )

    # If you want to align to custom freq bins (0:5:200), you can later
    # plot only f<=max or interpolate; keep it simple here.
    return f, t, Sxx
