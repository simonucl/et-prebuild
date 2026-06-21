# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="devops-task-prep" \
      Description="Environment for isolating 5xx HTTP responses from application logs"

# Update apt and install Python, pip, and dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    echo "Updating apt and installing Python + pip..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest via pip
RUN set -e && \
    echo "Installing pytest via pip..." && \
    python3 -m pip --no-cache-dir install --upgrade pip && \
    python3 -m pip --no-cache-dir install pytest

# Create directory structure and log file
RUN set -e && \
    echo "Creating directory structure and log file..." && \
    mkdir -p /home/user/projects/inventory/logs && \
    mkdir -p /home/user/reports

# Populate the application log using a heredoc
RUN cat >/home/user/projects/inventory/logs/app.log <<'EOF'
2023-10-21T23:59:59Z 10.0.0.1 GET /api/v1/orders 200 87ms
2023-10-22T00:00:01Z 10.0.0.2 GET /api/v1/orders 500 99ms
2023-10-22T01:15:30Z 10.0.0.3 POST /api/v1/login 200 45ms
2023-10-22T03:45:11Z 10.0.0.4 GET /api/v1/orders 502 120ms
2023-10-22T04:12:09Z 10.0.0.5 GET /api/v1/products 404 30ms
2023-10-22T09:30:00Z 10.0.0.6 GET /api/v1/orders 503 110ms
2023-10-22T12:00:00Z 10.0.0.7 GET /api/v1/orders 200 80ms
2023-10-22T15:23:45Z 10.0.0.8 GET /api/v1/orders 501 140ms
2023-10-22T18:47:55Z 10.0.0.9 GET /api/v1/orders 500 100ms
2023-10-22T22:59:59Z 10.0.0.10 GET /api/v1/orders 504 150ms
2023-10-23T00:00:01Z 10.0.0.11 GET /api/v1/orders 500 90ms
EOF

# Ensure appropriate permissions
RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/projects /home/user/reports && \
    chmod 644 /home/user/projects/inventory/logs/app.log

# Environment variables from Apptainer %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1