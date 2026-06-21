FROM ubuntu:22.04

# Environment variables
ENV PYTHONIOENCODING="utf-8"
ENV LC_ALL="C.UTF-8"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user/mlops_project

# Create the initial config.yml (only exp_001 present)
RUN cat > /home/user/mlops_project/config.yml <<'EOF'
experiments:
  - id: exp_001
    model: resnet50
    accuracy: 0.85
artifacts_dir: artifacts/
EOF

# Create the initial pyproject.toml
RUN cat > /home/user/mlops_project/pyproject.toml <<'EOF'
[tool.mymlpipe]
version = "0.1.0"
default_data_dir = "data/"
EOF

# Ensure the non-root user can modify everything inside /home/user
RUN chmod -R a+rwX /home/user

# Default action: open a shell unless something else is provided
CMD ["bash"]