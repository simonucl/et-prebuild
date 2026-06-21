# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---------------------------------------------------------------------
# Install Python tooling and pytest
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils && \
    pip3 install --no-cache-dir pytest

# ---------------------------------------------------------------------
# Prepare the required initial file-system state
# ---------------------------------------------------------------------
RUN mkdir -p /home/user/data/edge

RUN cat > /home/user/data/edge/sensor_raw.csv <<'EOF'
timestamp,device_id,tempC,humidity,pressurePa
2023-06-15T12:00:00Z,node-01,35.1,45,101325
2023-06-15T12:01:00Z,node-01,35.3,44,101327
2023-06-15T12:02:00Z,node-02,30.0,50,101300
2023-06-15T12:03:00Z,node-03,40.2,38,101400
EOF

# Allow the (non-root) runtime user to create files under /home/user
RUN chmod -R 777 /home/user

# Clean up APT caches to keep the image small
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*

# Labels (from %labels section)
LABEL Author="ChatGPT" \
      Description="Environment for the IoT edge-computing CSV extraction task, with pytest pre-installed"