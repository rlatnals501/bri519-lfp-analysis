from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

def plot_mean_lfp_overlay(
    ax,
    mean_low,
    mean_high,
    fs,
    title,
    stim_on_ms=100,
    stim_off_ms=150,
    ylabel="LFP (a.u., baseline-corrected)",
):
    t_ms = (np.arange(len(mean_low)) / fs) * 1000.0

    ax.plot(t_ms, mean_low, label="Low tone")
    ax.plot(t_ms, mean_high, label="High tone")

    # stimulus markers (midterm처럼)
    ax.axvline(stim_on_ms, linestyle="--", color="gray", label="Stim on")
    ax.axvline(stim_off_ms, linestyle=":", color="gray", label="Stim off")

    ax.set_title(title)
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel(ylabel)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)

def plot_psd_overlay(
    ax,
    f_low, pxx_low,
    f_high, pxx_high,
    title,
    max_freq_hz=200,
    ylabel="PSD (a.u.)",
    logy=True,
):
    m1 = f_low <= max_freq_hz
    m2 = f_high <= max_freq_hz

    ax.plot(f_low[m1], pxx_low[m1], label="Low tone")
    ax.plot(f_high[m2], pxx_high[m2], label="High tone")

    if logy:
        ax.set_yscale("log")

    ax.set_title(title)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel(ylabel)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)

def plot_spectrogram(ax, f: np.ndarray, t: np.ndarray, Sxx: np.ndarray, title: str, max_freq: float = 200.0):
    m = f <= max_freq
    im = ax.pcolormesh(t, f[m], Sxx[m, :], shading="auto")
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    return im