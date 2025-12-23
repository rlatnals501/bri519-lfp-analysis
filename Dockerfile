FROM python:3.11-slim

# Prevent interactive prompts and speed up
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (optional but helpful for scientific python)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency list first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY src /app/src
COPY README.md /app/README.md

# If you are committing the dataset:
# (recommended for this class if required)
COPY data /app/data

# Default command: run full pipeline
# Using PYTHONPATH=src so `lfp` is discoverable
CMD ["bash", "-lc", "PYTHONPATH=src python -m lfp.scripts.run_all --mat data/mouseLFP.mat --outdir results"]