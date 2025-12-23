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

src/lfp/ Core analysis modules
src/lfp/scripts/ Executable scripts
data/ Input data (mouseLFP.mat)
results/ Saved outputs and figures

---

## Installation

Create and activate a virtual environment, then install dependencies:

python -m venv .venv
source .venv/bin/activate # macOS/Linux

.venv\Scripts\activate # Windows
pip install -r requirements.txt

---

## Data

Place the dataset file in the following location:

data/mouseLFP.mat

The dataset is not included in this repository and must be obtained separately.

---

## Usage

Run the full analysis pipeline:

python -m lfp.scripts.run_all --mat data/mouseLFP.mat --outdir results

Run individual analysis methods:

python -m lfp.scripts.run_method1 --mat data/mouseLFP.mat --outdir results
python -m lfp.scripts.run_method2 --mat data/mouseLFP.mat --outdir results

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

## Notes

This project follows proper version control practices and modular refactoring.
Inline code comments and docstrings are provided throughout the source code to explain
the purpose, input/output structure, and key logic of core functions, including
outlier rejection, filtering, and time- and frequency-domain analyses.

Conceptual guidance and structural suggestions were informed using AI tools,
while all code implementation and analysis decisions were independently performed.