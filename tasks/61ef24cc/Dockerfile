# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels converted from %labels
LABEL Author="devops-container-generator" \
      Description="Apptainer image for mock API DevOps exercise (curl/jq/pytest prepared)" \
      Version="v1.0"

# Update apt cache and install required packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        jq \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest via pip
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create home directory, seed directories, and set permissions
RUN set -e && \
    mkdir -p /home/user/mock_api && \
    chmod 0777 /home/user

# ---------------------------------------------------------------------
# /home/user/mock_api/inventory.json
# ---------------------------------------------------------------------
RUN cat >/home/user/mock_api/inventory.json <<'EOF'
{
  "total_items": 3,
  "items": ["widget", "gadget", "doodad"]
}
EOF

# ---------------------------------------------------------------------
# /home/user/mock_api/user.json
# ---------------------------------------------------------------------
RUN cat >/home/user/mock_api/user.json <<'EOF'
{
  "users": [
    { "id": 1, "username": "alice" },
    { "id": 2, "username": "bob" }
  ]
}
EOF

# ---------------------------------------------------------------------
# /home/user/mock_api/health.txt (must end with a single LF)
# ---------------------------------------------------------------------
RUN printf 'OK\n' >/home/user/mock_api/health.txt

# Ensure world-readable permissions for the seed files
RUN chmod 0644 /home/user/mock_api/inventory.json && \
    chmod 0644 /home/user/mock_api/user.json && \
    chmod 0644 /home/user/mock_api/health.txt

# Runtime environment setup (from %environment)
RUN chmod 755 /home/user

# No special environment variables are required for this task.