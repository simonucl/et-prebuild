# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help section
# Basic OS preparation and filesystem setup for automated tests

ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/logs && \
    mkdir -p /home/user/.config/app

RUN cat <<'EOF' > /home/user/logs/app-2023-09-01.log
2023-09-01T08:15:27Z INFO download user=asmith file=document.pdf size=15234 ip=10.0.0.8
2023-09-01T09:01:11Z INFO rotateKey user=jdoe oldKey=abc123 ip=10.0.0.5
2023-09-01T09:05:14Z WARN cpu usage high
2023-09-01T10:22:47Z INFO rotateKey user=asmith oldKey=def456 ip=10.0.0.8
2023-09-01T11:45:22Z INFO rotateKey user=bwayne oldKey=ghi789 ip=10.0.0.9
2023-09-01T12:04:55Z INFO logout user=jdoe ip=10.0.0.5
EOF

RUN cat <<'EOF' > /home/user/logs/security_audit.log
2023-09-01:Audit start
EOF

RUN cat <<'EOF' > /home/user/.config/app/config.yml
apiEndpoint: "https://api.example.com/v1/"
apiKey: "abc123"
timeout: 30
EOF

RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/logs && \
    chmod -R 755 /home/user/.config && \
    chmod 644 /home/user/logs/*.log && \
    chmod 644 /home/user/.config/app/config.yml