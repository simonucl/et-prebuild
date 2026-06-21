# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# -------------------------------------------------------------------
# Base packages + pytest
# -------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------------
# Create initial directory tree and configuration files
# -------------------------------------------------------------------
RUN mkdir -p /home/user/netconfigs/old && \
    mkdir -p /home/user/netconfigs/new && \
    mkdir -p /home/user/etc

RUN cat > /home/user/netconfigs/old/router.conf <<'EOF'
hostname router-old
ip route 0.0.0.0/0 via 192.168.0.1
EOF

RUN cat > /home/user/netconfigs/new/router.conf <<'EOF'
hostname router-new
ip route 0.0.0.0/0 via 10.0.0.1
EOF

RUN cat > /home/user/netconfigs/old/switch.conf <<'EOF'
hostname switch-old
vlan 10
EOF

RUN cat > /home/user/netconfigs/new/switch.conf <<'EOF'
hostname switch-new
vlan 20
EOF

# -------------------------------------------------------------------
# Set up the (intentionally incorrect) “active” symlinks
# -------------------------------------------------------------------
RUN ln -sf /home/user/netconfigs/old/router.conf /home/user/etc/router.conf && \
    ln -sf /home/user/netconfigs/old/switch.conf /home/user/etc/switch.conf

# -------------------------------------------------------------------
# Permissions — make everything user-writable (non-root runtime)
# -------------------------------------------------------------------
RUN chmod -R a+rwX /home/user && \
    find /home/user -type d -exec chmod 0777 {} \;

# -------------------------------------------------------------------
# Environment setup (from %environment)
# -------------------------------------------------------------------
RUN chmod 755 /home/user
ENV HOME=/home/user

# -------------------------------------------------------------------
# Labels (from %labels)
# -------------------------------------------------------------------
LABEL Author="Network-Lab-Setup" \
      Description="Initial state for symlink-update exercise"

# -------------------------------------------------------------------
# Help (from %help)
# Container providing the starting environment for the symlink-update task.
# Directories and files under /home/user are created with write permissions
# so that an unprivileged agent can perform the required operations.
# -------------------------------------------------------------------