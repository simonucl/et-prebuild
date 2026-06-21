# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# -----------------------------------------------------------------
# Install Python tools and pytest
# -----------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------
# Prepare initial workspace expected by the tests
# -----------------------------------------------------------------
RUN set -e && \
    WORKDIR="/home/user/project/security" && \
    mkdir -p "${WORKDIR}"

# Create the initial firewall rules file with exactly two lines
RUN cat > "/home/user/project/security/firewall_rules.conf" <<'EOF'
22/tcp ALLOW
80/tcp ALLOW
EOF

# Ensure proper user-writable permissions (rw-r--r--)
RUN chmod 644 "/home/user/project/security/firewall_rules.conf"

# -----------------------------------------------------------------
# Environment setup
# -----------------------------------------------------------------
RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:$PATH"

# -----------------------------------------------------------------
# Labels
# -----------------------------------------------------------------
LABEL Author="example" \
      Description="Container providing the initial workspace for the firewall rules task with pytest pre-installed."