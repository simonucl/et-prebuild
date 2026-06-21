# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Post section: install dependencies and set up filesystem
# ------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create required directories and set permissions
RUN mkdir -p /home/user && \
    mkdir -p /home/user/provision && \
    chmod 0777 /home/user/provision

# Create servers.dat with exact required content
RUN cat >/home/user/provision/servers.dat <<'EOF'
hostname,role,dc
web01,app,dc1
db01,db,dc1
cache01,cache,dc2
EOF

# Create ips.dat with exact required content
RUN cat >/home/user/provision/ips.dat <<'EOF'
ip,netmask
10.0.0.11,255.255.255.0
10.0.0.21,255.255.255.0
10.0.0.31,255.255.255.0
EOF

# Ensure readable files and home permissions
RUN chmod 0644 /home/user/provision/servers.dat /home/user/provision/ips.dat && \
    chmod 755 /home/user

# ------------------------------------------------------------
# Environment section
# ------------------------------------------------------------
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH

# ------------------------------------------------------------
# Default command (runscript equivalent)
# ------------------------------------------------------------
CMD ["bash"]