# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the required directory structure
RUN mkdir -p /home/user/server_configs

# Create the INI configuration file
RUN cat > /home/user/server_configs/appserver.ini << 'EOF'
[web]
enabled = true
port = 8080

[db]
enabled = false
port = 5432

[cache]
enabled = true
port = 6379
EOF

# Ensure appropriate permissions
RUN chmod 1777 /home/user && \
    chmod 755  /home/user/server_configs && \
    chmod 644  /home/user/server_configs/appserver.ini

# Environment setup
ENV PATH=/usr/local/bin:$PATH

RUN chmod 755 /home/user && \
    if ! command -v python >/dev/null 2>&1; then \
        ln -sf /usr/bin/python3 /usr/local/bin/python; \
    fi

# Container run message
CMD echo "Container for the network-service INI parsing task."