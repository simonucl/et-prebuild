# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text from %help
# This container provides the initial filesystem state for the
# API-summary parsing task. It includes pytest for grading and an
# INI configuration file located at /home/user/api_configs/services.ini.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && \
    mkdir -p /home/user/api_configs

RUN cat <<'EOF' > /home/user/api_configs/services.ini
[UserService]
endpoint = https://api.example.com/users
token = abc123token
timeout = 30

[OrderService]
endpoint = https://api.example.com/orders
token = 987zyxTOKEN
timeout = 45

[InventoryService]
endpoint = https://api.example.com/inventory
token = invTOK456
timeout = 60
EOF

RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/api_configs && \
    chmod 0644 /home/user/api_configs/services.ini

LABEL Author="agent_setup"