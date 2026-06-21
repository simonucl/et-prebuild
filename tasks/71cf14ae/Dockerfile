FROM ubuntu:22.04

# Update package index and install required system packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        nodejs \
        npm \
        ca-certificates \
        git \
        curl

# Install Python testing framework
RUN pip3 install --no-cache-dir pytest

# Install markdownlint CLI (also provides the `markdownlint` command)
RUN npm install -g markdownlint-cli

# Prepare initial directory structure and seed files for the exercise
RUN mkdir -p /home/user/operator-manifests

# deployment.yaml
RUN cat > /home/user/operator-manifests/deployment.yaml <<'EOF'
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-deployment
  namespace: default
EOF

# service.yaml
RUN cat > /home/user/operator-manifests/service.yaml <<'EOF'
---
apiVersion: v1
kind: Service
metadata:
  name: sample-service
  namespace: default
EOF

# Ensure permissions so the non-root container user can work freely
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:$PATH"
ENV HOME="/home/user"

# Set working directory
WORKDIR /home/user

# Default command opens a shell
CMD ["/bin/bash"]