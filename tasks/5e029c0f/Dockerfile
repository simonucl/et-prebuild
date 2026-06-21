# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python tooling and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare the directory structure and seed the required raw log file
# ------------------------------------------------------------------
RUN mkdir -p /home/user/incidents/raw_logs

RUN cat > /home/user/incidents/raw_logs/network_2023-03-17.log <<'EOF'
2023-03-17T02:45:00Z 192.168.1.10 -> 10.23.45.67 TCP 450
2023-03-17T03:15:22Z 10.23.45.67 -> 192.168.1.10 TCP 1024
2023-03-17T03:45:10Z 10.23.45.67 -> 192.168.1.15 UDP 2048
2023-03-17T04:05:00Z 172.16.0.5 -> 10.23.45.67 TCP 300
2023-03-17T04:15:10Z 10.23.45.67 -> 192.168.1.20 TCP 512
2023-03-17T04:40:55Z 10.23.45.67 -> 192.168.1.30 TCP 256
2023-03-17T05:10:00Z 10.23.45.67 -> 192.168.1.35 UDP 400
EOF

# ------------------------------------------------------------------
# Ensure sensible permissions so the non-root agent can read the data
# ------------------------------------------------------------------
RUN chmod 644 /home/user/incidents/raw_logs/network_2023-03-17.log && \
    chmod -R 755 /home/user/incidents && \
    chmod 755 /home/user

LABEL Author="Container preparer for incident-response exercise"

# ------------------------------------------------------------------
# Help
# This container provides the initial filesystem state for the
# incident-response CSV-extraction task. The necessary raw log file
# is pre-loaded under /home/user/incidents/raw_logs/, and pytest is
# available for internal validation.
# ------------------------------------------------------------------