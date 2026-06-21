# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create initial dataset required by the task
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/data_project && \
    printf 'ALPHA BACKUP DATA\n' > /home/user/data_project/important.txt && \
    printf 'Original notes for the backup-restore test.\n' > /home/user/data_project/notes.md && \
    chmod -R a+rwX /home/user || true && \
    chown -R 1000:1000 /home/user || true

# ------------------------------------------------------------------
# Runtime environment setup
# ------------------------------------------------------------------
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8