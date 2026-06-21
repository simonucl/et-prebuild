FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create a non-privileged user
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g user -s /bin/bash user

# Set up initial directory structure and log files
RUN mkdir -p /home/user/api_logs && \
    printf "GET /v1/data 200 OK\n" > /home/user/api_logs/request.log && \
    printf "HTTP/1.1 200 OK\nContent-Type: application/json\n{ \"status\": \"ok\" }\n" > /home/user/api_logs/response.log && \
    printf "[Error] 504 Gateway Timeout at 2023-02-01T12:34:56Z\n" > /home/user/api_logs/errors.log

# Ownership and permissions
RUN chown -R 1000:1000 /home/user && \
    chmod 644 /home/user/api_logs/*.log && \
    chmod 755 /home/user

ENV PATH=/home/user/.local/bin:$PATH