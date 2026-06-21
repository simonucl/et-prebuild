FROM ubuntu:22.04

# Help / metadata from %labels
LABEL Author="Dummy Builder"
LABEL Description="Container with initial state for dummy_service configuration task"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-dev && \
    pip3 install --no-cache-dir pytest

# Prepare filesystem
RUN mkdir -p /home/user && \
    mkdir -p /home/user/configs && \
    chmod 0777 /home/user/configs

# Create dummy_service.conf via heredoc
RUN cat > /home/user/configs/dummy_service.conf <<'EOF'
#-----------------------------------
# Dummy Service configuration file
# Maintainer: DevOps Team
MAX_CLIENTS=50
#-----------------------------------
EOF

RUN chmod 0644 /home/user/configs/dummy_service.conf && \
    chmod 755 /home/user

ENV HOME=/home/user