# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python 3, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the exercise
RUN mkdir -p /home/user/security

# config.yaml with the old token
RUN cat > /home/user/security/config.yaml <<'EOF'
api:
  token: oldtoken123
  url: https://internal.example.com/api
EOF

# settings.toml with the old token
RUN cat > /home/user/security/settings.toml <<'EOF'
[api]
token = "oldtoken123"
url   = "https://internal.example.com/api"
EOF

# Make directory and files writable by the unprivileged user
RUN chmod 0777 /home/user/security && \
    chmod 0666 /home/user/security/config.yaml /home/user/security/settings.toml

# Environment setup (from %environment)
RUN mkdir -p /home/user && chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

LABEL Author="AI_Assistant" \
      Description="Apptainer image for credential-rotation task with pytest pre-installed"