# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python, pip, pytest, and create filesystem layout
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/artifact-manager/repos

# Create the configuration file using heredoc
RUN cat > /home/user/artifact-manager/artifact-manager.conf <<'EOF'
# Artifact Manager Configuration
[global]
storage_root = /home/user/artifact-manager/repos
EOF

# Fix permissions
RUN chmod -R 0777 /home/user/artifact-manager

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Additional environment rule
RUN chmod 755 /home/user