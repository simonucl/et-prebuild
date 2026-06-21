FROM ubuntu:22.04

# Maintainer compliance-task-setup
# Description "Environment for checksum-based audit trail task."
# This container sets up the initial state for the TLS certificate
# audit-trail exercise. It pre-installs pytest and stages a dummy
# certificate so that learners can generate the required SHA-256 log.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/compliance/certs && \
    mkdir -p /home/user/compliance/audit/trails

RUN printf 'abc' > /home/user/compliance/certs/server.crt

RUN chmod 755 /home/user && \
    chmod 755 /home/user/compliance && \
    chmod 755 /home/user/compliance/certs && \
    chmod 777 /home/user/compliance/audit/trails && \
    chmod 644 /home/user/compliance/certs/server.crt

LABEL Maintainer="compliance-task-setup" \
      Description="Environment for checksum-based audit trail task."