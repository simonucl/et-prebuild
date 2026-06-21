# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="AgentPrep" \
      Description="Pre-populated environment with legacy word-count script and sample data"

# Update package lists and install required tools
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gawk \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the runtime checker
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Set up legacy tools directory and its contents
# ------------------------------------------------------------------
RUN mkdir -p /home/user/legacy_tools

# word_count.sh – simple POSIX shell word counter
RUN cat > /home/user/legacy_tools/word_count.sh << 'EOS'
#!/bin/sh
# Simple POSIX shell script – counts words in a file passed as $1
wc -w "$1" | awk '{print $1}'
EOS

RUN chmod +x /home/user/legacy_tools/word_count.sh

# sample.txt – contains exactly six whitespace-separated words
RUN cat > /home/user/legacy_tools/sample.txt << 'EOS'
Hello world from legacy code base.
EOS

# Ensure sensible permissions so the non-privileged user can read them
RUN chmod 755 /home/user/legacy_tools && \
    chmod 644 /home/user/legacy_tools/sample.txt

# Environment variables from Apptainer %environment
ENV LC_ALL=C \
    PATH="/usr/local/bin:/usr/bin:/bin"

# %runscript equivalent:
# Container for legacy word-count task. Nothing to run by default.