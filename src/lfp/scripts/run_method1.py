import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

from lfp.config import LFPConfig
from lfp.io import load_mouse_lfp_mat
from lfp.outliers import baseline_outlier_mask, tone_indices
from lfp.filters import design_lowpass, apply_filtfilt
from lfp.analysis import compute_mean_lfp, compute_psd_welch
from lfp.save import ensure_dir


def main():
    parser = argparse.ArgumentParser(
        description="Run Method 1: Mean LFP and PSD analysis"
    )
    parser.add_argument("--mat", required=True, help="Path to mouseLFP.mat")
    parser.add_argument("--outdir", default="results", help="Output directory")
    args = parser.parse_args()

    cfg = LFPConfig()
    DATA = load_mouse_lfp_mat(args.mat)

    ensure_dir(args.outdir)

    # Design low-pass filter (same as MATLAB but 10th-order)
    b, a = design_lowpass(cfg.fs, cfg.cutoff_hz, cfg.filter_order)

    for s in range(cfg.num_sessions):
        # -----------------------------
        # 1. Load raw data (one session)
        # -----------------------------
        raw_trials = DATA[s, 0]          # (num_trials, num_samples)
        tone_info = DATA[s, 4].squeeze() # (num_trials,)

        # -----------------------------
        # 2. Baseline-based outlier rejection
        # -----------------------------
        keep_mask, out_info = baseline_outlier_mask(
            raw_trials,
            baseline_end=cfg.stim_onset_sample,
            k=cfg.outlier_k
        )

        raw_kept = raw_trials[keep_mask]

        # -----------------------------
        # 3. Low-pass filtering
        # -----------------------------
        filt_trials = apply_filtfilt(raw_kept, b, a)

        # -----------------------------
        # 4. Separate low / high tones
        # -----------------------------
        low_idx, high_idx, _, _ = tone_indices(tone_info)

        kept_indices = np.where(keep_mask)[0]
        low_rows = np.searchsorted(
            kept_indices,
            np.intersect1d(kept_indices, low_idx)
        )
        high_rows = np.searchsorted(
            kept_indices,
            np.intersect1d(kept_indices, high_idx)
        )

        low_trials = filt_trials[low_rows]
        high_trials = filt_trials[high_rows]

        # -----------------------------
        # 5. Mean LFP
        # -----------------------------
        mean_low = compute_mean_lfp(low_trials)
        mean_high = compute_mean_lfp(high_trials)

        # -----------------------------
        # 6. PSD (Welch)
        # -----------------------------
        f_low, pxx_low = compute_psd_welch(mean_low, cfg.fs)
        f_high, pxx_high = compute_psd_welch(mean_high, cfg.fs)

        # -----------------------------
        # 7. Plot (match midterm style)
        # -----------------------------
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        plot_mean_lfp_overlay(
            axes[0],
            res["mean_low"],
            res["mean_high"],
            cfg.fs,
            title=f"Session {s+1} - Mean LFP (Time domain)",
            stim_on_ms=100,
            stim_off_ms=150,
        )

        plot_psd_overlay(
            axes[1],
            res["psd"]["f_low"],  res["psd"]["pxx_low"],
            res["psd"]["f_high"], res["psd"]["pxx_high"],
            title=f"Session {s+1} - Post-stimulus PSD (Frequency domain)",
            max_freq_hz=cfg.max_freq_hz,
            logy=True,
        )

        fig.suptitle(f"Session {s+1} - Method 1 (Mean LFP & PSD)")
        fig.tight_layout()
        fig.savefig(os.path.join(args.outdir, f"session{s+1}_method1.png"), dpi=200)
        plt.close(fig)

if __name__ == "__main__":
    main()
