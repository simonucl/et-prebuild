FROM ubuntu:22.04

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install Python, pip, pytest, and useful CLI tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the required initial filesystem state
RUN mkdir -p /home/user/data

RUN cat > /home/user/data/deployments.csv <<'EOF'
namespace,app,image,replicas
default,api-server,nginx:1.21,3
prod,worker,python:3.10,5
dev,frontend,node:14,2
EOF

# Set the correct permissions
RUN chmod 755 /home/user/data && \
    chmod 644 /home/user/data/deployments.csv

# Runscript message as comment
# Container for the Kubernetes CSV summarisation task.
# Start an interactive shell with: docker exec -it <container> /bin/bash

CMD ["/bin/bash"]