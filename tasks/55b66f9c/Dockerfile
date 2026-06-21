# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python, pip, and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial filesystem state for the exercise
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/site-config && \
    chmod -R 0777 /home/user

# Create the initial users.conf file with the required four lines
RUN cat > /home/user/site-config/users.conf <<'EOF'
alice:admin
bob:editor
charlie:viewer
diana:viewer
EOF

# Make the file writable by the learner
RUN chmod 0666 /home/user/site-config/users.conf

# ------------------------------------------------------------------
# Environment configuration
# ------------------------------------------------------------------
ENV PYTHONIOENCODING=utf-8

RUN chmod 755 /home/user

# ------------------------------------------------------------------
# Runtime behavior
# ------------------------------------------------------------------
CMD echo "Container for the 'users.conf' editing task." && \
    echo "Run your commands to modify /home/user/site-config/users.conf as specified." && \
    exec "$@"

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
# This container sets up the initial state for the configuration-editing task.
# 1. The directory /home/user/site-config/ exists and is writable.
# 2. /home/user/site-config/users.conf contains the initial four lines.
# 3. pytest is installed for automated verification.