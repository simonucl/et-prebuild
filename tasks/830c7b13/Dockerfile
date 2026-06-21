# This container supplies the tooling required for the “SQLite provisioning demo” task:
#   • sqlite3 CLI
#   • Python 3 and pytest (for the autograder)
# The provisioning directory /home/user/provisioning/db is intentionally absent.

FROM ubuntu:22.04

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user