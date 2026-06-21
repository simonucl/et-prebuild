# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Labels (from %labels)
# ------------------------------------------------------------------
LABEL Author="Apptainer Task Generator" \
      Description="Container for point-in-time backup exercise. Provides initial project files and pytest."

# ------------------------------------------------------------------
# Post section (%post)
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the forthcoming autograder
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare initial project structure required by the assignment
RUN mkdir -p /home/user/project/env

# Create configuration files with the exact content specified
RUN printf 'version=1.0\n' > /home/user/project/app.conf && \
    printf 'host=localhost\nport=5432\n' > /home/user/project/db.conf && \
    printf 'DEBUG=true\n'   > /home/user/project/env/dev.env && \
    printf 'DEBUG=false\n'  > /home/user/project/env/prod.env

# Make the directory tree world-writable so the unprivileged learner UID
# (unknown at build time) can freely create archives, logs, etc.
RUN chmod -R a+rwX /home/user

# ------------------------------------------------------------------
# Environment section (%environment)
# ------------------------------------------------------------------
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    HOME=/home/user

# ------------------------------------------------------------------
# Help section (%help)
# ------------------------------------------------------------------
# Container for point-in-time backup exercise.
# Provides initial project files and pytest.