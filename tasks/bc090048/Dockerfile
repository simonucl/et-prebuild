# syntax=docker/dockerfile:1
# Author check-sums task setup
# Description: Prepares initial state for checksum verification exercise
# This container image sets up the initial filesystem state required for the
# checksum verification coding task and includes pytest so that the automated
# grader can validate both the initial state and the student’s solution.

FROM ubuntu:22.04

ENV HOME=/home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/config_backups

RUN printf 'abc' > /home/user/config_backups/fw01.conf && \
    printf 'hello world' > /home/user/config_backups/sw02.conf && \
    : > /home/user/config_backups/rtr03.conf

RUN cat > /home/user/config_backups/reference_checksums.csv <<'EOF'
FILENAME,SHA256
fw01.conf,ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
sw02.conf,b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
rtr03.conf,e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/config_backups && \
    chmod 644 /home/user/config_backups/*