FROM ubuntu:22.04

# Labels
LABEL Author="Container Auto-Builder"
LABEL Description="Environment for the world-writable file enumeration task with pytest pre-installed."

# Install Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem layout required by the autograder
RUN mkdir -p /home/user/app && \
    chmod 0755 /home/user/app

# 1. config.yml (0644)
RUN cat <<'EOF' > /home/user/app/config.yml
# Example configuration for the prototype web-app
database: sqlite:///db.sqlite
EOF

RUN chmod 0644 /home/user/app/config.yml

# 2. db.sqlite (0666 — world-writable)
RUN : > /home/user/app/db.sqlite && \
    chmod 0666 /home/user/app/db.sqlite

# 3. script.sh (0755)
RUN cat <<'EOF' > /home/user/app/script.sh
#!/usr/bin/env bash
echo "Hello, World!"
EOF

RUN chmod 0755 /home/user/app/script.sh

# Ensure /home/user itself exists and is accessible
RUN chmod 0755 /home/user || true

# Environment variables
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /home/user