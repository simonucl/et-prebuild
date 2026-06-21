# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------ #
# 1. Base packages and pytest
# ------------------------------------------------------------------ #
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-venv \
        ca-certificates \
        bash \
        coreutils && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------ #
# 2. Create non-privileged user 'user'
# ------------------------------------------------------------------ #
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# ------------------------------------------------------------------ #
# 3. Pre-existing secops structure & credential file
# ------------------------------------------------------------------ #
RUN install -d -o user -g user /home/user/secops

RUN cat > /home/user/secops/credentials_2023-12-01.csv <<'EOF'
username,service,credential_id,created_at,expires_at
alice,db,credA1,2023-12-01,2024-06-01
bob,web,credB2,2023-12-01,2024-06-01
carol,api,credC3,2023-12-01,2024-06-01
EOF

RUN chown user:user /home/user/secops/credentials_2023-12-01.csv && \
    chmod 0644 /home/user/secops/credentials_2023-12-01.csv

# ------------------------------------------------------------------ #
# Environment setup
# ------------------------------------------------------------------ #
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:$PATH"

# ------------------------------------------------------------------ #
# Labels
# ------------------------------------------------------------------ #
LABEL Author="Apptainer build script" \
      Description="Initial state container for credential-rotation exercise"

# ------------------------------------------------------------------ #
# Help
# ------------------------------------------------------------------ #
# This image provides the initial filesystem layout required
# for the credential-rotation task. It contains:
#   • User  : 'user' (UID/GID 1000)
#   • Folder: /home/user/secops/
#   • File  : credentials_2023-12-01.csv (original credential set)
#
# The archive/ and rotation_logs/ folders DO NOT exist yet—those will be
# created during the exercise.
#
# Pytest is installed system-wide for validation purposes.