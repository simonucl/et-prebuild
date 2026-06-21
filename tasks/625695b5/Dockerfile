# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        rsync && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial filesystem state expected by the autograder
# ------------------------------------------------------------------

# Create home directory
RUN mkdir -p /home/user

# 1. Source project with the required structure and files
RUN mkdir -p /home/user/source_project/assets && \
    printf '<!-- version 1 -->\n'  > /home/user/source_project/index.html && \
    printf '// version 1\n'        > /home/user/source_project/script.js && \
    printf '/* version 1 */\n'     > /home/user/source_project/assets/style.css

# 2. Empty backup directory
RUN mkdir -p /home/user/backup_server

# 3. rsync log directory (world-writable for the non-root user who will run tests)
RUN mkdir -p /home/user/rsync_logs && \
    chmod 0777 /home/user/rsync_logs

# Set sensible permissions on the rest
RUN chmod -R 0755 /home/user/source_project && \
    chmod 0755 /home/user/backup_server && \
    chmod 0755 /home/user

# Environment variables
ENV LC_ALL=C
ENV PYTHONIOENCODING=UTF-8