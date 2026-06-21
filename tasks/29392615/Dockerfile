FROM ubuntu:22.04

# Help documentation:
# This container provides the initial workspace and dependencies for the
# YAML/TOML registry editing exercise. Pytest is pre-installed so that the
# grading tests can run inside the container.

# Install Python and pytest
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory hierarchy
RUN mkdir -p /home/user/project/experiments && \
    mkdir -p /home/user/project/artifacts

# Create the initial registry.yaml with the exact 7 lines expected
RUN cat > /home/user/project/experiments/registry.yaml <<'EOF'
experiments:
  - id: exp_001
    artifact_path: /home/user/project/artifacts/exp_001
    commit: a1b2c3d
  - id: exp_002
    artifact_path: /home/user/project/artifacts/exp_002
    commit: d4e5f6g
EOF

# Ensure the non-root user (who will run inside the container) has
# full access to everything under /home/user.
RUN chmod -R a+rwX /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user

# Default command: drop into a shell if the container is executed
CMD ["/bin/bash"]