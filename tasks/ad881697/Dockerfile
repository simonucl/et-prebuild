# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        coreutils && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project/data /home/user/project/src && \
    : > /home/user/project/README.md && \
    : > /home/user/project/data/sample.txt && \
    : > /home/user/project/src/main.py

RUN cat <<'EOF' > /home/user/project/checksums.sha256
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  README.md
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  data/sample.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  src/main.py
EOF

RUN cat <<'EOF' > /home/user/project/checksum_verification.log
README.md: OK
data/sample.txt: OK
src/main.py: OK
EOF

RUN chmod -R a+rX /home/user

LABEL Author="example@example.com"
LABEL Description="Container for checksum-manifest exercise (pytest preinstalled)"