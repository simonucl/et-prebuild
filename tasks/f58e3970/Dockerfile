FROM ubuntu:22.04

# Help text
# This container provides the baseline environment for the rollout-venv
# task. Python, the venv module, and pytest are available. No initial
# artefacts (virtual environment or setup.log) are created, so the task
# begins with a clean slate.

LABEL Author="Apptainer setup for rollout venv task"
LABEL Description="Ubuntu 22.04 image with Python, venv support, and pytest pre-installed."
LABEL Version="1.0"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user