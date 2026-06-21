FROM ubuntu:22.04

# Labels
LABEL Author="Binary-Repo-Task"
LABEL Description="Base container for the binary-repository management exercise"

# Basic tooling
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential && \
    # Install pytest for the checker
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    # Clean up apt caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the exercise
# Create the dedicated, non-privileged user (UID/GID 1000)
RUN if ! getent group 1000 >/dev/null; then \
        groupadd -g 1000 user; \
    fi && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -g 1000 -d /home/user user; \
    fi

# Staging directory with empty binary files
RUN mkdir -p /home/user/temp/artifacts && \
    touch /home/user/temp/artifacts/toolA-1.0.bin && \
    touch /home/user/temp/artifacts/toolB-2.5.bin && \
    touch /home/user/temp/artifacts/utilC-0.9.bin && \
    # Ensure the learner can freely write under /home/user
    chmod -R a+rwX /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"