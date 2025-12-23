```markdown
# BRI519 Mouse LFP Analysis

This project refactors a midterm assignment into a modular and reproducible Python project.
It analyzes local field potential (LFP) recordings from mouse auditory cortex in response to
low- and high-frequency auditory tone stimuli across four experimental sessions.

---

## Project Overview

The analysis pipeline consists of the following steps:

1. Load raw LFP data from `mouseLFP.mat`
2. Perform baseline-based outlier trial rejection (0–100 ms pre-stimulus)
3. Apply a 10th-order Butterworth low-pass filter (cutoff frequency: 1000 Hz)
4. Conduct main analyses:
   - **Method 1**: Mean LFP waveform (time domain) and power spectral density (frequency domain)
   - **Method 2**: Time–frequency analysis using spectrograms

---

## Project Structure

- `src/lfp/` — Core analysis modules
- `src/lfp/scripts/` — Executable scripts
- `data/` — Input data (`mouseLFP.mat`)
- `results/` — Saved outputs and figures

---

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---


## Data

Place the dataset file in the following location:
```bash
data/mouseLFP.mat
```
The dataset is not included in this repository and must be obtained separately.

---

## Usage

All scripts should be executed from the project root directory.

Because the source code is located under the src/ directory, please use the following
command format:
```bash
PYTHONPATH=src python -m lfp.scripts.run_all --mat data/mouseLFP.mat --outdir results
```
Run individual analysis methods:
```bash
PYTHONPATH=src python -m lfp.scripts.run_method1 --mat data/mouseLFP.mat --outdir results
PYTHONPATH=src python -m lfp.scripts.run_method2 --mat data/mouseLFP.mat --outdir results
```
---

## Output

All analysis outputs are saved under the `results/` directory, including:

- Raw LFP data
- Low-pass filtered LFP data
- Baseline-based outlier trial masks
- Mean LFP waveforms
- Power spectral density (PSD) results
- Time–frequency spectrograms

Outputs are stored in both NumPy (`.npz`) and MATLAB-compatible (`.mat`) formats to ensure
reproducibility and cross-platform compatibility.

---

### Running the Code

All scripts should be executed from the project root directory.

Because the source code is located under the `src/` directory, please use the
following command format:

PYTHONPATH=src python -m lfp.scripts.run_all --mat data/mouseLFP.mat --outdir results

---

## Notes

This project follows proper version control practices and modular refactoring.
The original exploratory analysis was conducted in a Jupyter notebook, and the
finalized analysis pipeline was refactored into modular Python scripts to improve
reusability, readability, and maintainability.

Inline code comments and docstrings are provided throughout the source code to explain
the purpose, input/output structure, and key logic of core functions, including
outlier rejection, filtering, and time- and frequency-domain analyses.

AI tools (ChatGPT) were used to assist with high-level method brainstorming.
All coding, analysis, and decision-making processes were conducted independently
by the author.

---

## Fixes, Debugging, and Validation

Several issues identified during the refactoring and modularization process
were systematically resolved to ensure correct and stable execution of the
analysis pipeline.

First, mismatches between function definitions and function calls were fixed.
In particular, the spectrogram computation initially included an unnecessary
argument that was not consistently passed across modules, resulting in runtime
errors. The function interface was simplified to rely on SciPy’s native frequency
handling, resolving the issue and improving code clarity.

Second, module import errors were addressed by restructuring the project into a
proper Python package and enforcing a consistent execution pattern
(`PYTHONPATH=src python -m lfp.scripts.<script_name>`). This ensured that all
modules were discoverable and executable from the command line.

Third, the execution logic was reorganized into multiple entry scripts to improve
clarity and usability. Separate scripts were implemented for running individual
analysis methods (`run_method1.py` and `run_method2.py`), while a unified script
(`run_all.py`) was designed to execute the complete analysis pipeline in a single
command. This structure allows both modular testing of each method and end-to-end
execution of the full workflow.

Finally, the data storage mechanism was validated by confirming that all outputs
are correctly saved in appropriate formats, including per-session NumPy files
(`.npz`), session-level visualization figures (`.png`), and a MATLAB-compatible
summary file (`.mat`). All scripts were executed successfully without errors,
confirming that the refactored pipeline functions as intended.