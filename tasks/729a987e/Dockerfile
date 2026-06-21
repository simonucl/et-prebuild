# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ===============================
# Install required packages
# ===============================
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ===============================
# Prepare initial filesystem
# ===============================
RUN mkdir -p /home/user/myapp

RUN cat > /home/user/myapp/config.ini <<'EOF'
[service]
name=myapp
port=8080
debug=false
EOF

# Make everything under /home/user writable for the non-root runtime user
RUN chmod -R a+rwX /home/user

# ===============================
# Environment configuration
# ===============================
# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# Ensure that 'python' resolves to Python 3
ENV PATH=/usr/local/bin:/usr/bin:/bin

# ===============================
# Help / description
# ===============================
# This container provides a basic Python 3 environment with pytest installed
# and an example application configuration under /home/user/myapp/config.ini