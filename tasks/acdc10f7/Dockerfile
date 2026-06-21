# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling for pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the non-root user expected by the exercise
RUN set -eux && \
    if ! getent group 1000 >/dev/null; then \
        groupadd -g 1000 user; \
    fi && \
    if ! id -u 1000 >/devnull 2>&1; then \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# Prepare the initial Kubernetes manifest files
RUN mkdir -p /home/user/manifests

RUN cat <<'EOF' >/home/user/manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-deployment
  namespace: demo
EOF

RUN cat <<'EOF' >/home/user/manifests/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-service
  namespace: demo
EOF

# Ensure the files and directories belong to the non-root user
RUN chown -R 1000:1000 /home/user

# Corresponding to %environment
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Labels
LABEL Author="your_name"
LABEL Description="Container for Kubernetes manifest documentation exercise"