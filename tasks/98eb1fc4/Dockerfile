FROM ubuntu:22.04

# Help:
# This container provides the environment for the Grafana “latency-overview”
# tuning confirmation exercise. Pytest is pre-installed, and a writable
# /home/user directory is available for the student.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

LABEL Author="Observability-Exercise"
LABEL Description="Base image for latency-overview tuning exercise (pytest included)"