FROM ubuntu:22.04

# Help text
# This container provides the initial state for the mock-API smoke-test
# programming exercise.

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN set -eux && \
    mkdir -p /home/user/mock_api && \
    chmod 0777 /home/user && \
    chmod 0755 /home/user/mock_api

RUN printf '{"users":[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]}' > /home/user/mock_api/users.json && \
    chmod 0644 /home/user/mock_api/users.json

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

LABEL Author="AI Assistant"
LABEL Description="Environment for mock-API smoke-test task"