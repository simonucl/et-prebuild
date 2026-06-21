FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Initialiser"
LABEL Description="Container preparing initial state for credential-rotation challenge"
LABEL Version="1.0"

# Update package lists and install Python with pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-privileged user `user` (UID/GID 1000) and its home
RUN groupadd -g 1000 user && \
    useradd -m -s /bin/bash -u 1000 -g 1000 user

# Populate the expected initial file structure
RUN mkdir -p /home/user/app && \
    mkdir -p /home/user/logs

# config.yaml with the old credentials
RUN cat > /home/user/app/config.yaml <<'EOF'
---
app_name: sampleapp
database:
  user: appuser
  password: changeme123
logging:
  level: info
---
EOF

# secret.toml with the old token
RUN cat > /home/user/app/secret.toml <<'EOF'
# Internal secrets
[api]
token = "changeme123"
EOF

# Permissions: make sure the `user` account owns everything and that
# /home/user/logs is writable by anyone (no root needed later)
RUN chown -R 1000:1000 /home/user && \
    chmod 0777 /home/user/logs && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"