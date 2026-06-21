FROM ubuntu:22.04

# Help:
# This container supplies the minimal tools needed for the “network-diagnostics”
# task. It includes:
#   • iputils-ping for unprivileged ICMP probes
#   • pytest for automated grading
# The directory /home/user is pre-created and writable; no task‑specific
# artefacts are present so the initial state is clean.

LABEL Author="Exercise Maintainer"
LABEL Description="Starter image for the network-diagnostics exercise with ping and pytest pre-installed."

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iputils-ping \
        python3-pip \
        ca-certificates \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin