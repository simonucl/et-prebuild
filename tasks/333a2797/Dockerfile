FROM ubuntu:22.04

# Help text
# This container image provides the initial dataset and Python/pytest
# tooling required for the integration-backend log processing exercise.

# Labels
LABEL Author="YourName"
LABEL Description="Environment for the awk/sed log-processing task (pytest included)"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/api_test/logs

RUN cat <<'EOF' > /home/user/api_test/logs/access.log
2024-04-01T10:00:01Z 192.168.1.10 GET /v1/users 200 123
2024-04-01T10:00:02Z 192.168.1.11 POST /v1/login 201 87
2024-04-01T10:00:03Z 192.168.1.12 POST /v1/orders 503 232
2024-04-01T10:00:04Z 192.168.1.13 GET /v1/products 200 145
2024-04-01T10:00:05Z 192.168.1.14 POST /v1/orders 500 310
2024-04-01T10:00:06Z 192.168.1.15 GET /v1/users 404 99
2024-04-01T10:00:07Z 192.168.1.16 POST /v1/login 502 120
2024-04-01T10:00:08Z 192.168.1.17 GET /v1/products 200 98
EOF

RUN chmod -R 0777 /home/user/api_test

RUN chmod 755 /home/user