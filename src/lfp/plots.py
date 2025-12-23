from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

def plot_mean_lfp(ax, mean_trace: np.ndarray, fs: float, title: str):
    t_ms = np.arange(mean_trace.size) / fs * 1000.0
    ax.plot(t_ms, mean_trace)
    ax.set_title(title)
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Amplitude")

def plot_psd(ax, f: np.ndarray, pxx: np.ndarray, title: str, max_freq: float = 200.0):
    m = f <= max_freq
    ax.plot(f[m], pxx[m])
    ax.set_title(title)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Power")

def plot_spectrogram(ax, f: np.ndarray, t: np.ndarray, Sxx: np.ndarray, title: str, max_freq: float = 200.0):
    m = f <= max_freq
    im = ax.pcolormesh(t, f[m], Sxx[m, :], shading="auto")
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    return im
