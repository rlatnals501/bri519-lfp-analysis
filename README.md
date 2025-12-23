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

## Getting Started
First, clone the repository and move into the project directory:
```bash
git clone https://github.com/kimsumin/BRI519-LFP-ANALYSIS.git
cd BRI519-LFP-ANALYSIS
```

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
- Per-session numerical results (`session*_results.npz`)
- Mean LFP and PSD figures (`session*_method1.png`)
- Time–frequency spectrograms (`session*_method2.png`)
- MATLAB-compatible summary file (`lfp_analysis_results.mat`)
Outputs are stored in both NumPy (`.npz`) and MATLAB-compatible (`.mat`) formats to ensure
reproducibility and cross-platform compatibility.

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

---

## Docker Setup & Usage

This project is fully containerized using Docker to ensure reproducible execution of the LFP analysis pipeline.

1. Build the Docker Image

Clone the repository and build the Docker image locally:
```bash
git clone https://github.com/rlatnals501/bri519-lfp-analysis.git
cd BRI519-LFP-ANALYSIS

docker build -t bri519-lfp:latest .
```
`bri519-lfp` is the local image name.
You may change it if needed.

2. Run the Docker Container

Run the full analysis pipeline (equivalent to `run_all.py`) using Docker:
```bash
docker run --rm -v "$PWD/data:/app/data" -v "$PWD/results:/app/results" bri519-lfp:latest
```
Explanation
- `--rm` : Automatically remove the container after execution
- `-v "$PWD/data:/app/data"` : Mount input data directory
- `-v "$PWD/results:/app/results"` : Mount output results directory
- All analysis results (`.png`, `.npz`, `.mat`) will be saved to `results/`

3. Docker Hub Image
The pre-built Docker image is available on Docker Hub:
```bash
https://hub.docker.com/r/rlatnals501/bri519-lfp
```
You can pull and run the image directly without building it locally:
```bash
docker pull rlatnals501/bri519-lfp:final

docker run --rm -v "$PWD/data:/app/data" -v "$PWD/results:/app/results" rlatnals501/bri519-lfp:final
```

4. Reproducibility Note
The Docker container includes all required Python dependencies.
Running the container produces identical outputs to local execution.
The analysis entry point is configured via the Docker CMD to execute:
```bash
PYTHONPATH=src python -m lfp.scripts.run_all --mat data/mouseLFP.mat --outdir results
```