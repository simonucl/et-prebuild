# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package index and install Python, pip, and pytest for testing
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Scaffold required project structure for the student.
# Only the /home/user/app directory and the .env.sample file
# should exist at image-start. Nothing else requested by the
# assignment (e.g., .env, logs/, env_debug.log) is created here.
# ------------------------------------------------------------------

RUN mkdir -p /home/user/app && \
    chmod 755 /home/user/app

RUN cat >/home/user/app/.env.sample <<'EOF'
API_KEY=__REPLACE_ME__
APP_ENV=__REPLACE_ME__
LOG_LEVEL=__REPLACE_ME__
SERVICE_PORT=__REPLACE_ME__
EOF

RUN chmod 644 /home/user/app/.env.sample

# ------------------------------------------------------------------
# Runtime notes (from %runscript in Apptainer)
# Container for environment-variable setup task.
# Invoke an interactive shell with:  docker run -it <image> /bin/bash
# or run tests with:               pytest -q
# ------------------------------------------------------------------