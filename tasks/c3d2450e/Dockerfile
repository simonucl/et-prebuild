# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# This container provides the initial filesystem state for the “CI/CD log-trimming”
# exercise. Three raw build logs are pre-seeded in /home/user/ci_logs/.
# Learners must generate trimmed error files and a summary TSV using awk/sed.

# Install system packages and Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create directory structure and set permissions
RUN mkdir -p /home/user/ci_logs && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/ci_logs

# Seed build_backend_20230912.log
RUN cat <<'EOF' > /home/user/ci_logs/build_backend_20230912.log
[INFO] Starting backend build
[INFO] Fetching dependencies
[ERROR] Missing dependency: libfoo
[INFO] Retrying...
[ERROR] Missing dependency: libfoo
[INFO] Build failed
EOF

# Seed build_frontend_20230912.log
RUN cat <<'EOF' > /home/user/ci_logs/build_frontend_20230912.log
[INFO] Starting frontend build
[INFO] Installing packages
[INFO] Compiling TypeScript
[ERROR] Can't resolve './App'
[ERROR] Can't resolve './Header'
[INFO] Build failed
EOF

# Seed build_docs_20230912.log
RUN cat <<'EOF' > /home/user/ci_logs/build_docs_20230912.log
[INFO] Starting docs build
[INFO] Generating docs
[INFO] Docs build completed successfully
EOF

# Fix log permissions
RUN chmod 0666 /home/user/ci_logs/*.log

# Environment configuration
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN chmod 755 /home/user

# Labels
LABEL Author="CI-Task-Generator"
LABEL Description="Environment for CI/CD log-trimming exercise with pytest pre-installed."