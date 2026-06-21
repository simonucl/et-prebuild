# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic tools and Python runtime
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Testing framework required by the checker
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare the initial filesystem state expected by the assignment
# ------------------------------------------------------------------
# Create home and manifests directory
RUN mkdir -p /home/user/manifests

RUN cat <<'EOF' > /home/user/manifests/web-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: myapp/web:v1
EOF

RUN cat <<'EOF' > /home/user/manifests/cache-deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cache
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cache
  template:
    metadata:
      labels:
        app: cache
    spec:
      containers:
      - name: cache
        image: myapp/cache:v1
EOF

# Permissions
RUN chmod 777 /home/user && \
    chmod 755 /home/user/manifests && \
    chmod 644 /home/user/manifests/*.yaml

# ------------------------------------------------------------------
# Environment variables
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONIOENCODING=utf-8