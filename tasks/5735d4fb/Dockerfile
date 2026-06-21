# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install required packages
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        diffutils && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create the initial directory structure
# ------------------------------------------------------------------
RUN mkdir -p /home/user/pipeline_configs/old && \
    mkdir -p /home/user/pipeline_configs/new

# ------------------------------------------------------------------
# Old pipeline configuration
# ------------------------------------------------------------------
RUN cat > /home/user/pipeline_configs/old/config.yml <<'EOF'
version: "1.0"
stages:
  - build
  - test
  - deploy
EOF

# ------------------------------------------------------------------
# New pipeline configuration
# ------------------------------------------------------------------
RUN cat > /home/user/pipeline_configs/new/config.yml <<'EOF'
version: "1.1"
stages:
  - build
  - test
  - deploy
notifications:
  email: devops@example.com
EOF

# ------------------------------------------------------------------
# Set permissions
# ------------------------------------------------------------------
RUN chmod 777 /home/user && \
    chmod -R 755 /home/user/pipeline_configs

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="container-builder" \
      Description="Initial state for CI/CD patch generation task"

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
# This container sets up the baseline environment for the CI/CD patch
# generation exercise. The necessary old and new configuration files are
# located under /home/user/pipeline_configs. Students must create their
# patch and log under /home/user/ci_cd_patch.