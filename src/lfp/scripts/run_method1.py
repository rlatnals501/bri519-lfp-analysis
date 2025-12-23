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
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        t_ms = np.arange(mean_low.size) / cfg.fs * 1000

        axes[0, 0].plot(t_ms, mean_low, color="k")
        axes[0, 0].set_title(f"Session {s+1} Low Tone - Mean LFP")
        axes[0, 0].set_xlabel("Time (ms)")
        axes[0, 0].set_ylabel("Amplitude")

        axes[0, 1].plot(t_ms, mean_high, color="k")
        axes[0, 1].set_title(f"Session {s+1} High Tone - Mean LFP")
        axes[0, 1].set_xlabel("Time (ms)")

        m = f_low <= cfg.max_freq_hz
        axes[1, 0].plot(f_low[m], pxx_low[m])
        axes[1, 0].set_title("Low Tone PSD")
        axes[1, 0].set_xlabel("Frequency (Hz)")
        axes[1, 0].set_ylabel("Power")

        m = f_high <= cfg.max_freq_hz
        axes[1, 1].plot(f_high[m], pxx_high[m])
        axes[1, 1].set_title("High Tone PSD")
        axes[1, 1].set_xlabel("Frequency (Hz)")

        fig.tight_layout()
        fig.savefig(
            os.path.join(args.outdir, f"session{s+1}_method1.png"),
            dpi=200
        )
        plt.close(fig)


if __name__ == "__main__":
    main()
