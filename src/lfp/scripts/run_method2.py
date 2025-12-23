import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal.windows import hann

from lfp.config import LFPConfig
from lfp.io import load_mouse_lfp_mat
from lfp.outliers import baseline_outlier_mask, tone_indices
from lfp.filters import design_lowpass, apply_filtfilt
from lfp.analysis import compute_mean_lfp
from lfp.tf import compute_spectrogram
from lfp.save import ensure_dir


def main():
    parser = argparse.ArgumentParser(
        description="Run Method 2: Time-Frequency Spectrogram analysis"
    )
    parser.add_argument("--mat", required=True, help="Path to mouseLFP.mat")
    parser.add_argument("--outdir", default="results", help="Output directory")
    args = parser.parse_args()

    cfg = LFPConfig()
    DATA = load_mouse_lfp_mat(args.mat)
    ensure_dir(args.outdir)

    b, a = design_lowpass(cfg.fs, cfg.cutoff_hz, cfg.filter_order)

    window = hann(256)
    noverlap = 255

    for s in range(cfg.num_sessions):
        # -----------------------------
        # 1. Load raw data
        # -----------------------------
        raw_trials = DATA[s, 0]
        tone_info = DATA[s, 4].squeeze()

        # -----------------------------
        # 2. Outlier rejection
        # -----------------------------
        keep_mask, _ = baseline_outlier_mask(
            raw_trials,
            baseline_end=cfg.stim_onset_sample,
            k=cfg.outlier_k
        )

        raw_kept = raw_trials[keep_mask]

        # -----------------------------
        # 3. Filtering
        # -----------------------------
        filt_trials = apply_filtfilt(raw_kept, b, a)

        # -----------------------------
        # 4. Tone separation
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
        # 6. Spectrogram
        # -----------------------------
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        for ax, sig, label in zip(
            axes,
            [mean_low, mean_high],
            ["Low Tone", "High Tone"]
        ):
            f, t, Sxx = compute_spectrogram(
                sig, cfg.fs, window, noverlap
            )

            m = f <= cfg.max_freq_hz
            im = ax.pcolormesh(
                t, f[m], Sxx[m, :], shading="auto"
            )
            ax.set_title(f"Session {s+1} {label} Spectrogram")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Frequency (Hz)")
            fig.colorbar(im, ax=ax)

        fig.tight_layout()
        fig.savefig(
            os.path.join(args.outdir, f"session{s+1}_method2.png"),
            dpi=200
        )
        plt.close(fig)


if __name__ == "__main__":
    main()
