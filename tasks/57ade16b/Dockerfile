# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Labels (from %labels)
# ------------------------------------------------------------------
LABEL Author="container-prep bot"
LABEL Description="Environment for the 'mock_api build-and-publish' task"

# ------------------------------------------------------------------
# Base tooling
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        curl \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Python testing framework
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare task resources
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user && \
    mkdir -p /home/user/mock_api

# Artifact A
RUN cat > /home/user/mock_api/artifactA.json <<'EOF'
{
  "artifact": "library-core",
  "version": "1.4.2",
  "checksum": "3b7f3aaf79be67fcb10"
}
EOF

# Artifact B
RUN cat > /home/user/mock_api/artifactB.json <<'EOF'
{
  "artifact": "service-api",
  "version": "2.0.0",
  "checksum": "7dcb73d9ce5fa26c881"
}
EOF

# Permissions and cleanup
RUN set -e && \
    chmod -R 755 /home/user/mock_api && \
    chmod 755 /home/user && \
    rm -rf /home/user/build_outputs || true

# ------------------------------------------------------------------
# Environment variables (from %environment)
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8