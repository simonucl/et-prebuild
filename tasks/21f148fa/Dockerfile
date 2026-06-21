FROM ubuntu:22.04

# Help text
# This container provides the initial state for the checksum logging task.

LABEL Author="YourName"
LABEL Description="Container for checksum-ledger task; includes pytest and pre-populated model.bin"

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/experiments/run_42

RUN printf 'hello' > /home/user/experiments/run_42/model.bin

RUN chmod -R a+rwX /home/user/experiments

RUN chmod 755 /home/user