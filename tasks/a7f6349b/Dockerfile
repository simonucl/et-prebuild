# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / metadata
LABEL Author="build-automation-prep"
LABEL Description="Base container for build-environment task: ensures /home/user is writable and pytest is available"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Updating package index and installing required tools..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    echo "Creating the /home/user directory with permissive permissions..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    if ! command -v python >/dev/null 2>&1; then ln -s /usr/bin/python3 /usr/local/bin/python; fi

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Runscript equivalent
CMD echo "Container for build-environment task. Invoke your shell or command explicitly."