from __future__ import annotations
import numpy as np
from scipy.io import loadmat

def load_mouse_lfp_mat(mat_path: str) -> np.ndarray:
    """
    Load mouseLFP.mat and return MATLAB cell array DATA as a numpy object array.

    Returns
    -------
    DATA : np.ndarray (num_sessions, num_fields) object array
        DATA[s, 0] -> raw LFP trials (num_trials, num_samples)
        DATA[s, 4] -> tone labels/values (num_trials,)
    """
    mat = loadmat(mat_path)
    if "DATA" not in mat:
        raise KeyError("Expected key 'DATA' in .mat file.")
    return mat["DATA"]
