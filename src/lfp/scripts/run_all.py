import argparse
import os

import matplotlib.pyplot as plt
from scipy.signal.windows import hann

from lfp.config import LFPConfig
from lfp.io import load_mouse_lfp_mat
from lfp.pipeline import LFPPipeline
from lfp.plots import plot_mean_lfp_overlay, plot_psd_overlay
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
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        plot_mean_lfp_overlay(
            axes[0],
            res["mean_low"],
            res["mean_high"],
            cfg.fs,
            title=f"Mean LFP (Time domain)",
            stim_on_ms=100,
            stim_off_ms=150,
        )

        plot_psd_overlay(
            axes[1],
            res["psd"]["f_low"],  res["psd"]["pxx_low"],
            res["psd"]["f_high"], res["psd"]["pxx_high"],
            title=f"Post-stimulus PSD (Frequency domain)",
            max_freq_hz=cfg.max_freq_hz,
            logy=True,
        )

        fig.suptitle(f"Session {s+1} - Method 1 (Mean LFP & PSD)")
        fig.tight_layout()
        fig.savefig(os.path.join(args.outdir, f"session{s+1}_method1.png"), dpi=200)
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
