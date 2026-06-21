FROM ubuntu:22.04

# Help:
# This container supplies:
#   • ssh-keygen (from openssh-client) for RSA key creation
#   • pytest for automated grading
#   • A writable /home/user directory for the learner’s work

# Author: security-log-analyst-prep
# Description: Environment for SSH-key generation exercise (pytest pre-checks installed)

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        openssh-client \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user