# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install system dependencies, Python, pip, and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        build-essential && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare the initial dataset expected by the exercise
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/data/experiment

RUN cat > /home/user/data/experiment/requirements_raw.txt <<'EOF'
numpy==1.23.5
pandas==1.5.3
scipy==1.9.3
numpy==1.23.5
matplotlib==3.6.2
EOF

# Ensure correct permissions – world-writable so the unprivileged agent
# (whose UID/GID are unknown at build time) can create new files.
RUN set -e && \
    chmod 644 /home/user/data/experiment/requirements_raw.txt && \
    chmod -R 777 /home/user/data && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment variables (from %environment)
# ------------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ------------------------------------------------------------------
# %runscript (informational)
# Container for the requirements-cleanup exercise.
# Open a shell (docker run -it ...) to begin working.
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# %test (placeholder)
# ------------------------------------------------------------------