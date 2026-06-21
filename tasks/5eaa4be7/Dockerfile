# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---------------------------------------------------------------------
# Install required Python testing framework
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------
# Create initial project directory tree
# ---------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/project/backend && \
    mkdir -p /home/user/project/deploy && \
    mkdir -p /home/user/project/infra

# ---------------------------------------------------------------------
# backend/.env
# ---------------------------------------------------------------------
RUN cat > /home/user/project/backend/.env <<'EOF'
# Local development variables
DATABASE_URL="postgres://user:pass@localhost:5432/app"
AWS_SECRET_ACCESS_KEY="AKIA111111111EXAMPLE"
AWS_ACCESS_KEY_ID="ASIA11111111EXAMPLE"
DEBUG=true
EOF

# ---------------------------------------------------------------------
# deploy/k8s.env
# ---------------------------------------------------------------------
RUN cat > /home/user/project/deploy/k8s.env <<'EOF'
# Staging cluster variables
KUBE_CONTEXT="staging"
AWS_SECRET_ACCESS_KEY="AKIA222222222EXAMPLE"
EOF

# ---------------------------------------------------------------------
# infra/secrets.env
# ---------------------------------------------------------------------
RUN cat > /home/user/project/infra/secrets.env <<'EOF'
# Terraform backend
STATE_BUCKET="terraform-state"
AWS_SECRET_ACCESS_KEY="AKIA333333333EXAMPLE"
AWS_REGION="us-east-1"
EOF

# ---------------------------------------------------------------------
# Adjust permissions so the unprivileged runtime user can write under /home/user
# ---------------------------------------------------------------------
RUN chmod -R 0777 /home/user

# ---------------------------------------------------------------------
# Labels (from %labels section)
# ---------------------------------------------------------------------
LABEL Author="ChatGPT" \
      Description="Apptainer image for AWS credential leak scanning exercise"

# ---------------------------------------------------------------------
# Help (from %help section)
# This container provides the initial filesystem state for the AWS credential
# scanning exercise. It pre-installs pytest (used by the automated grader) and
# sets up the project directory tree under /home/user with the required sample
# files.
# ---------------------------------------------------------------------