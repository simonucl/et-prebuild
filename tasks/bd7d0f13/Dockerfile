# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="BuildEngineer"
LABEL Description="Base image for the offline Python artifact bundle exercise."

ENV PATH="${PATH}:/home/user/.local/bin"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN groupadd -r user && \
    useradd -r -g user -m -d /home/user -s /bin/bash user

RUN mkdir -p /home/user/package_repo

RUN python3 - <<'PY'
import subprocess, sys
dest = "/home/user/package_repo"
pkgs = [
    "colorama==0.4.6",
    "humanfriendly==10.0",
    "pytz==2023.3",
]
subprocess.check_call([sys.executable, "-m", "pip", "download",
                       "--no-deps", "--dest", dest] + pkgs)
PY

RUN cd /home/user/package_repo && \
    expected="colorama-0.4.6|humanfriendly-10.0|pytz-2023.3" && \
    count=0 && \
    for w in *.whl; do \
        case "$w" in \
            colorama-0.4.6-*.whl|humanfriendly-10.0-*.whl|pytz-2023.3-*.whl) ;; \
            *) echo "Unexpected wheel found: $w"; exit 1 ;; \
        esac; \
        count=$((count + 1)); \
    done && \
    [ "$count" -eq 3 ] || { echo "Expected 3 wheels, found $count"; exit 1; }

RUN chown -R user:user /home/user && \
    chmod 755 /home/user /home/user/package_repo

# Original runscript:
# echo "Container for the offline-bundle task is ready."
# echo "Switch to the expected user with:"
# echo "  apptainer exec --pwd /home/user --userns ${SINGULARITY_CONTAINER} /bin/bash"