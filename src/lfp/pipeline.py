from __future__ import annotations
import numpy as np
from dataclasses import asdict
from .config import LFPConfig
from .outliers import baseline_outlier_mask, tone_indices
from .filters import design_lowpass, apply_filtfilt
from .analysis import compute_mean_lfp, compute_psd_welch

class LFPPipeline:
    """
    Orchestrates outlier rejection, filtering, and analysis in a reusable form.
    """

    def __init__(self, cfg: LFPConfig):
        self.cfg = cfg
        self.b, self.a = design_lowpass(cfg.fs, cfg.cutoff_hz, cfg.filter_order)

    def process_session(self, DATA: np.ndarray, session_idx: int) -> dict:
        raw = DATA[session_idx, 0]              # (num_trials, num_samples)
        tone = DATA[session_idx, 4].squeeze()   # (num_trials,)

        keep_mask, out_info = baseline_outlier_mask(
            raw, baseline_end=self.cfg.stim_onset_sample, k=self.cfg.outlier_k
        )

        raw_kept = raw[keep_mask]
        filt_kept = apply_filtfilt(raw_kept, self.b, self.a)

        low_idx, high_idx, low_val, high_val = tone_indices(tone)

        # indices relative to original trials; convert to kept trials mask:
        kept_indices = np.where(keep_mask)[0]
        kept_low = np.intersect1d(kept_indices, low_idx, assume_unique=False)
        kept_high = np.intersect1d(kept_indices, high_idx, assume_unique=False)

        # map back to filt_kept rows:
        low_rows = np.searchsorted(kept_indices, kept_low)
        high_rows = np.searchsorted(kept_indices, kept_high)

        low_trials = filt_kept[low_rows]
        high_trials = filt_kept[high_rows]

        mean_low = compute_mean_lfp(low_trials)
        mean_high = compute_mean_lfp(high_trials)

        fL, pL = compute_psd_welch(mean_low, fs=self.cfg.fs)
        fH, pH = compute_psd_welch(mean_high, fs=self.cfg.fs)

        return {
            "config": asdict(self.cfg),
            "session_idx": session_idx,
            "outlier_info": out_info,
            "keep_mask": keep_mask,
            "tone_values": {"low": low_val, "high": high_val},
            "raw_kept": raw_kept,
            "filtered_kept": filt_kept,
            "filtered_low_trials": low_trials,
            "filtered_high_trials": high_trials,
            "mean_low": mean_low,
            "mean_high": mean_high,
            "psd": {"f_low": fL, "pxx_low": pL, "f_high": fH, "pxx_high": pH},
        }
