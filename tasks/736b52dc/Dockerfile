# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="YourName"
LABEL Description="Container for JSON-lines cleaning task with pytest and jq pre-installed."

# ------------------------------------------------------------------
# Install system dependencies and Python packages
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        jq \
        ca-certificates \
        --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest via pip (latest stable)
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create initial filesystem state expected by the grading tests
# ------------------------------------------------------------------

# Ensure /home/user and raw_data exist
RUN mkdir -p /home/user/raw_data

# Create the JSON-Lines file
RUN cat > /home/user/raw_data/people_raw.json <<'EOF'
{"id": 1, "name": "Alice", "age": 34}
{"id": 2, "name": "Bob", "age": 28}
{"id": 3, "name": "Charlie"}
{"name": "Faythe", "age": 29}
{"id": 4, "name": "Dana", "age": 45}
{"id": 5, "name": "Evan", "age": 31}
EOF

# Ensure clean_data and logs do NOT exist
RUN rm -rf /home/user/clean_data /home/user/logs

# ------------------------------------------------------------------
# Set permissions: directories 755, files 644
# ------------------------------------------------------------------
RUN chmod 755 /home/user && \
    chmod 755 /home/user/raw_data && \
    chmod 644 /home/user/raw_data/people_raw.json

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

# ------------------------------------------------------------------
# Help (from Apptainer %help)
# This image provides the initial environment for the data-cleaning
# assignment. It includes:
#   - /home/user/raw_data/people_raw.json (source JSON-Lines file)
#   - jq, python3, pip, and pytest pre-installed.
# The clean_data and logs directories are intentionally absent and
# should be created by the student during the task.
# ------------------------------------------------------------------