from dataclasses import dataclass

@dataclass(frozen=True)
class LFPConfig:
    fs: int = 10000
    cutoff_hz: float = 1000.0
    filter_order: int = 10

    bin_width_hz: float = 5.0
    max_freq_hz: float = 200.0

    num_sessions: int = 4
    num_trials: int = 200

    stim_onset_sample: int = 1000   # 100 ms at fs=10kHz
    stim_offset_sample: int = 1500  # 150 ms at fs=10kHz

    outlier_k: float = 5.0  # threshold = median + k*MAD
