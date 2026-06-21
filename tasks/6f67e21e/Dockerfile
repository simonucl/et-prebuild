# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="dev"
LABEL Description="Provision initial state for microservice config editing task with pytest installed"

# %post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user `user` (UID 1000 is conventional)
RUN useradd -m -u 1000 -s /bin/bash user

# Directory structure for the exercise
RUN install -d -o user -g user -m 0755 /home/user/microservices/api && \
    install -d -o user -g user -m 0700 /home/user/microservices/worker

# Initial deployment.yaml (0644)
RUN cat > /home/user/microservices/api/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  labels:
    app: api
    version: "v1"
spec:
  replicas: 2
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
        version: "v1"
    spec:
      containers:
        - name: api
          image: registry.example.com/api:v1.3.4
          env: []
EOF

RUN chown user:user /home/user/microservices/api/deployment.yaml && \
    chmod 0644 /home/user/microservices/api/deployment.yaml

# Ensure ownership of the entire home tree
RUN chown -R user:user /home/user

# Permissions adjustment from %environment
RUN chmod 755 /home/user

# %environment section
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

# %help
# This container sets up the initial filesystem and tooling required for the
# micro-service configuration editing exercise.