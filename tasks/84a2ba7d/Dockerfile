FROM ubuntu:22.04

# Labels
LABEL Author="Container build for server patch compliance task"
LABEL Version="1.0"

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install Python tooling for the tests
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory hierarchy
RUN mkdir -p /home/user/systems && \
    mkdir -p /home/user/compliance

# Populate the pre-existing patch status file
RUN cat > /home/user/systems/patch_status.txt <<'EOF'
serverA,current
serverB,outdated
serverC,current
serverD,outdated
serverE,current
EOF

# Set permissions: readable for all; writable where needed for the agent
RUN chmod 755 /home/user && \
    chmod 755 /home/user/systems && \
    chmod 777 /home/user/compliance && \
    chmod 644 /home/user/systems/patch_status.txt