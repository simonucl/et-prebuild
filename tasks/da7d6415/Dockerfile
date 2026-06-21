FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT – Apptainer build script"
LABEL Description="Ubuntu 22.04 image with Python, pip, and pytest for the package snapshot task."

# Help information (as comments)
# This container is prepared for the "pip freeze snapshot" exercise.
# It provides Python 3, pip, and pytest.  No backup directory or file
# has been created so the learner can perform the required steps.

# Install packages and setup
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pytest
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Prepare a writable home directory for the student/user
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Intentionally DO NOT create /home/user/archives or any backup file.
# These are to be created by the learner during the exercise.

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

WORKDIR /home/user