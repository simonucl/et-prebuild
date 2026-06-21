FROM ubuntu:22.04

# From %help / %labels
LABEL Author="fictitious@example.com"
LABEL Description="Setup for the 'suspicious file checksum' exercise"

# 1. Install Python tooling and pytest
RUN set -eux; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates; \
    pip3 install --no-cache-dir pytest; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*

# 2. Prepare filesystem layout
RUN set -eux; \
    mkdir -p /home/user; \
    chmod 0755 /home/user; \
    INCIDENT_DIR="/home/user/incident_artifacts"; \
    mkdir -p "${INCIDENT_DIR}"; \
    chmod 0755 "${INCIDENT_DIR}"; \
    touch "${INCIDENT_DIR}/suspicious.bin"; \
    chmod 0644 "${INCIDENT_DIR}/suspicious.bin"

# From %environment (chmod must be RUN, exports become ENV)
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8