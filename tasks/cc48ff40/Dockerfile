FROM ubuntu:22.04

# Author="Release-Manager Exercise Setup"
# Description="Environment for the release-manager text-processing task with pytest installed."

# This container provides the starting filesystem and tools (cut, paste, pytest)
# required for the "release-manager" exercise.

RUN set -eu && \
    echo "Updating package index and installing required packages..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        coreutils \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating initial directory structure and seed files..." && \
    install -d -m 0755 /home/user/releases/logs

RUN cat > /home/user/releases/environments.csv <<'EOF'
env,owner
prod,alice
staging,bob
qa,charlie
EOF

RUN cat > /home/user/releases/versions.txt <<'EOF'
prod v2.3.1
staging v2.3.1-rc
qa v2.3.0
EOF

RUN chmod 0644 /home/user/releases/environments.csv /home/user/releases/versions.txt && \
    chmod 755 /home/user && \
    echo "Container setup complete."