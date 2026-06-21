# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="backup-integrity-setup" \
      Description="Initial state for the Backup-Integrity exercise"

# Install system dependencies and Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        ca-certificates \
        git \
        locales && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create the dedicated working directory structure
RUN mkdir -p /home/user/data_backup/2023-11-01

# Seed files with the exact byte contents required by the tests
# 1. db.sql  -> 3 bytes "abc"
RUN printf 'abc' > /home/user/data_backup/2023-11-01/db.sql

# 2. photos.tar.gz  -> 5 bytes "hello"
RUN printf 'hello' > /home/user/data_backup/2023-11-01/photos.tar.gz

# 3. docs.zip -> empty file
RUN : > /home/user/data_backup/2023-11-01/docs.zip

# Adjust permissions so the non-root runtime user can read everything
RUN chmod -R a+rX /home/user && \
    chmod 755 /home/user

# Environment variables from %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command: open a shell so the automated agent can operate
CMD ["/bin/bash"]

# Help:
# This image provides the pristine starting environment for the
# “backup-integrity” exercise. It contains:
#   • The seed backup files under /home/user/data_backup/2023-11-01
#   • Python 3 and pytest for automated evaluation
#   • ssh-keygen (from openssh-client) for key-pair generation
#
# No SSH keys or integrity-report artefacts exist yet; students are expected
# to create them during the task.