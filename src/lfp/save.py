from __future__ import annotations
import os
import numpy as np
from scipy.io import savemat

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def save_npz(path: str, **kwargs):
    ensure_dir(os.path.dirname(path))
    np.savez_compressed(path, **kwargs)

def save_mat(path: str, data: dict):
    ensure_dir(os.path.dirname(path))
    savemat(path, data)
