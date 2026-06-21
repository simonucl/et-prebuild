# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# This image contains the starting files for the credential-rotation task:
#   /home/user/rotate/old_creds.csv – the pre-populated credential list.
# Students must generate new_creds.csv and rotation.log inside the same
# directory using standard shell utilities. Pytest is already installed for
# automated grading.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/rotate

RUN cat > /home/user/rotate/old_creds.csv <<'CSV_EOF'
username,password,expiration
alice,pa55w0rd!,2023-03-01
bob,letMeIn123,2023-04-15
carol,S3cur3Key#,2023-05-30
CSV_EOF

RUN chmod 777 /home/user/rotate && \
    chmod 644 /home/user/rotate/old_creds.csv && \
    chmod 755 /home/user

ENV PATH="${PATH}:${HOME}/.local/bin"

LABEL Author="container-prep"
LABEL Description="Initial state container for the credential-rotation exercise."