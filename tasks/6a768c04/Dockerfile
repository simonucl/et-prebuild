# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest, set up filesystem, and clean up
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/legacy_configs

# Create initial configuration file using heredoc
RUN cat >/home/user/legacy_configs/payment_service.conf <<'EOF'
SERVICE_NAME=payment
SERVICE_PORT=8080
DB_HOST=localhost
DB_PORT=5432
EOF

# Ensure the student can write inside /home/user
RUN chmod -R 0777 /home/user

# Clean up apt caches to reduce image size
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*

# Labels from Apptainer definition
LABEL Author="ExampleAuthor" \
      Description="Initial state for migration assignment with pytest installed"