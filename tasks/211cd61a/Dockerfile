# Converted from Apptainer definition
# Help:
# This container provides the runtime environment for the “CPU-intensive process snapshot” incident‑response exercise.
# Key points:
# • Python 3 and pytest are installed for automated grading.
# • /home/user exists and is world‑writable so the learner can create required artifacts.
# • The ir_logs directory and top_cpu.log file are intentionally absent; the student must create them.

FROM ubuntu:22.04

# Update and install packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        procps \
        --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip install --no-cache-dir pytest

# Create home directory
RUN mkdir -p /home/user && chmod 0777 /home/user

# Environment settings
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH

# Apply chmod from %environment
RUN chmod 755 /home/user

# Labels
LABEL Author="Incident Response Exercise Image"
LABEL Description="Base image for CPU snapshot task. Contains Python, pytest, and a writable /home/user."