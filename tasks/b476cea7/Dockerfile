# syntax=docker/dockerfile:1
# Equivalent to: Bootstrap: localimage / From: ./ubuntu_22.04.sif
FROM ubuntu:22.04

# Update apt repositories and install dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        jq \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create the CI directory structure
RUN mkdir -p /home/user/ci

# Write JSON payload
RUN cat > /home/user/ci/pipeline_payload.json <<'EOF'
{
  "pipeline": {
    "id": 42,
    "status": "succeeded",
    "stages": ["build", "test", "deploy"],
    "commit": {
      "hash": "a1b2c3d4",
      "author": "devops"
    }
  }
}
EOF

# Ensure directory writable
RUN chmod -R 777 /home/user

# From %environment (commands cannot be in ENV; apply chmod via RUN)
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8