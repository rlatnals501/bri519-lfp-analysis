import argparse
import os

import matplotlib.pyplot as plt
from scipy.signal.windows import hann

from lfp.config import LFPConfig
from lfp.io import load_mouse_lfp_mat
from lfp.pipeline import LFPPipeline
from lfp.plots import plot_mean_lfp, plot_psd
from lfp.tf import compute_spectrogram
from lfp.save import save_npz, save_mat, ensure_dir


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mat", required=True, help="Path to mouseLFP.mat")
    parser.add_argument("--outdir", default="results", help="Output directory")
    args = parser.parse_args()

    cfg = LFPConfig()
    DATA = load_mouse_lfp_mat(args.mat)

    pipe = LFPPipeline(cfg)

    ensure_dir(args.outdir)
    session_reports = []

    # Method 2 spectrogram parameters (match midterm)
    window = hann(256)
    noverlap = 255

    for s in range(cfg.num_sessions):
        res = pipe.process_session(DATA, s)
        session_reports.append(res["outlier_info"])

        # -----------------------------
        # Save per-session data (npz)
        # -----------------------------
        save_npz(
            os.path.join(args.outdir, f"session{s+1}_results.npz"),
            keep_mask=res["keep_mask"],
            mean_low=res["mean_low"],
            mean_high=res["mean_high"],
            f_low=res["psd"]["f_low"],
            pxx_low=res["psd"]["pxx_low"],
            f_high=res["psd"]["f_high"],
            pxx_high=res["psd"]["pxx_high"],
        )

        # -----------------------------
        # Plot per-session Method 1 (mean LFP + PSD)
        # -----------------------------
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        plot_mean_lfp(
            axes[0, 0],
            res["mean_low"],
            cfg.fs,
            f"Session {s+1} Low tone - Mean LFP",
        )
        plot_mean_lfp(
            axes[0, 1],
            res["mean_high"],
            cfg.fs,
            f"Session {s+1} High tone - Mean LFP",
        )
        plot_psd(
            axes[1, 0],
            res["psd"]["f_low"],
            res["psd"]["pxx_low"],
            f"Session {s+1} Low tone - PSD",
            cfg.max_freq_hz,
        )
        plot_psd(
            axes[1, 1],
            res["psd"]["f_high"],
            res["psd"]["pxx_high"],
            f"Session {s+1} High tone - PSD",
            cfg.max_freq_hz,
        )
        fig.tight_layout()
        fig.savefig(os.path.join(args.outdir, f"session{s+1}_method1.png"), dpi=200)
        plt.close(fig)

        # -----------------------------
        # Plot per-session Method 2 (spectrogram)
        # -----------------------------
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        for ax, mean_sig, label in zip(
            axes,
            [res["mean_low"], res["mean_high"]],
            ["Low tone", "High tone"],
        ):
            f, t, Sxx = compute_spectrogram(mean_sig, cfg.fs, window, noverlap)
            m = f <= cfg.max_freq_hz

            im = ax.pcolormesh(t, f[m], Sxx[m, :], shading="auto")
            ax.set_title(f"Session {s+1} {label} Spectrogram")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Frequency (Hz)")
            fig.colorbar(im, ax=ax)

        fig.tight_layout()
        fig.savefig(os.path.join(args.outdir, f"session{s+1}_method2.png"), dpi=200)
        plt.close(fig)

    # -----------------------------
    # Save combined summary (.mat)
    # -----------------------------
    save_mat(
        os.path.join(args.outdir, "lfp_analysis_results.mat"),
        {"session_outlier_report": session_reports},
    )


if __name__ == "__main__":
    main()
