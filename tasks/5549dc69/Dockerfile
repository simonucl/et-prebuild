FROM ubuntu:22.04

# Labels
LABEL Author="Observability-Setup"
LABEL Description="Environment for slow-endpoints exercise"

# Post installation
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip python3-setuptools python3-wheel \
        gzip ca-certificates \
        coreutils && \
    groupadd --gid 1000 user && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash user && \
    mkdir -p /home/user/observability/logs && \
    mkdir -p /home/user/observability/report

# Create the plaintext log file using heredoc
RUN cat > /tmp/app-2023-09-21.log <<'EOF'
2023-09-20T11:00:00Z GET /health 200 15ms
2023-09-21T13:58:01Z GET /api/v1/users 200 120ms
2023-09-21T13:59:01Z GET /api/v1/users 200 180ms
2023-09-21T14:00:01Z GET /api/v1/users 200 100ms
2023-09-21T14:00:05Z POST /api/v1/orders 201 220ms
2023-09-21T14:01:01Z GET /api/v1/users 200 140ms
2023-09-21T14:01:05Z POST /api/v1/orders 201 260ms
2023-09-21T14:02:05Z POST /api/v1/orders 201 240ms
2023-09-21T14:02:10Z POST /api/v1/payments 201 310ms
2023-09-21T14:03:10Z POST /api/v1/payments 201 290ms
2023-09-21T14:04:10Z GET /api/v1/inventory 200 80ms
2023-09-21T14:04:20Z GET /api/v1/inventory 200 90ms
2023-09-21T14:04:30Z GET /api/v1/carts 200 150ms
2023-09-21T14:05:30Z GET /api/v1/carts 200 170ms
EOF

# Compress log file and set permissions
RUN set -eux && \
    OBS_ROOT="/home/user/observability" && \
    gzip -c /tmp/app-2023-09-21.log > "${OBS_ROOT}/logs/app-2023-09-21.log.gz" && \
    rm /tmp/app-2023-09-21.log && \
    chown -R user:user /home/user && \
    chmod 0755 /home/user/observability && \
    chmod 0755 /home/user/observability/logs && \
    chmod 0755 /home/user/observability/report && \
    chmod 0644 "${OBS_ROOT}/logs/app-2023-09-21.log.gz"

# Install pytest for the grader/tests
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Environment variables
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Container for slow-endpoints exercise. Drop into a shell with: docker exec -u user <container> /bin/bash"]