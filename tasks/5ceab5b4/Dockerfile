# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Task Setup – Release Manager Staging Exercise"

# ------------------------------------------------------------------
# Post section: install dependencies and prepare filesystem
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare directory structure
RUN mkdir -p /home/user/releases/apps/service_a && \
    mkdir -p /home/user/releases/apps/service_b

# Initial deployment.yaml (NO staging block yet)
RUN cat >/home/user/releases/apps/service_a/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: service-a
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: service-a
    spec:
      containers:
        - name: service-a
          image: registry.example.com/service-a:1.4.2
          resources:
            limits:
              memory: "256Mi"
              cpu: "500m"
EOF

# Initial release.toml (NO [release.staging] table yet)
RUN cat >/home/user/releases/apps/service_b/release.toml <<'EOF'
[package]
name = "service_b"
version = "2.0.0"
checksum = "abcdef123456"
repository = "https://git.example.com/service_b.git"

[dependencies]
logger = "1.0"
database = "3.2"
EOF

# Ensure non-root users inside the container can read/write these files
RUN chmod -R u+rwX,go+rX /home/user && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment section
# ------------------------------------------------------------------
ENV PYTHONIOENCODING="UTF-8"