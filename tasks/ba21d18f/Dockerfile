FROM ubuntu:22.04

# Labels
LABEL Author="Student"
LABEL Description="Container for FinOps loop-back latency test – provides ping, Python, and pytest."

# Help information (as comments):
# This image supplies:
#   • iputils-ping  – standard ICMP diagnostics tool
#   • Python 3      – runtime for student scripts
#   • pytest        – testing framework used by the automated grader
#
# The /home/user directory is pre-created and world-writable so that
# unprivileged users can generate required artefacts during grading.

# Post installation commands
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
ENV LC_ALL=C.UTF-8

WORKDIR /home/user