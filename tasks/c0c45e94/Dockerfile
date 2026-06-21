# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Basic tools and Python environment
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create a regular, non-root user with UID/GID 1000
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 user || true

# Build the required initial filesystem layout
RUN mkdir -p /home/user/microservices && \
    chown 1000:1000 /home/user/microservices && \
    chmod 0755 /home/user/microservices

# Populate the CSV inventory
RUN cat > /home/user/microservices/services.csv <<'EOF'
service_name,image,port
auth-service,ghcr.io/org/auth:1.0,8080
payment-service,ghcr.io/org/pay:1.0,9090
frontend,ghcr.io/org/front:2.1,80
EOF

RUN chown 1000:1000 /home/user/microservices/services.csv && \
    chmod 0644 /home/user/microservices/services.csv

# Environment setup
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:${PATH}"

# Default runscript behavior
CMD ["bash"]