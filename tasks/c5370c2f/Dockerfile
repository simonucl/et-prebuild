# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install required Python packages
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir pytest pyyaml tomli

# Create configuration directory
RUN mkdir -p /home/user/repositories/config && \
    chmod 755 /home/user/repositories/config

# Create repo-settings.yaml
RUN cat > /home/user/repositories/config/repo-settings.yaml <<'YAML_EOF'
repositories:
  - name: "core-libs"
    type: "maven"
    url: "https://artifacts.example.com/libs-release-local"
  - name: "plugins"
    type: "npm"
    url: "https://artifacts.example.com/npm"
YAML_EOF
RUN chmod 644 /home/user/repositories/config/repo-settings.yaml

# Create cleanup-policy.toml
RUN cat > /home/user/repositories/config/cleanup-policy.toml <<'TOML_EOF'
[policy]
active = true
maxDays = 60
TOML_EOF
RUN chmod 644 /home/user/repositories/config/cleanup-policy.toml

# Ensure the edit log does not exist
RUN rm -f /home/user/repositories/config/config-edit.log

# Environment variables
ENV PYTHONUSERBASE=/home/user/.local
ENV PATH=/home/user/.local/bin:$PATH

# Help (from %runscript)
# Container for the artifact-manager exercise.
# Run your commands inside an interactive shell:
#     apptainer exec <container>.sif /bin/bash