FROM ubuntu:22.04

# Author: Apptainer Task Prep Bot
# Description: Base image for the “monitoring-alerts” exercise with pytest pre-installed.

LABEL Author="Apptainer Task Prep Bot" \
      Description="Base image for the monitoring-alerts exercise with pytest pre-installed."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"