FROM ubuntu:22.04

# Labels
LABEL Author="example_builder"
LABEL Description="Base container for compression/archiving task; includes pytest and initial directory state."

###############################
# 1. Install Python & pytest  #
###############################
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

###############################
# 2. Prepare initial filesystem
###############################
# Create base home directory with open permissions so the
# unprivileged runtime user can create / modify files inside.
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# --- /home/user/scripts ---------------------------------------
RUN mkdir -p /home/user/scripts && \
    chmod 0755 /home/user/scripts

# hello.sh
RUN cat > /home/user/scripts/hello.sh <<'EOF'
#!/usr/bin/env bash
echo "Hello, World!"
EOF

RUN chmod 0755 /home/user/scripts/hello.sh

# README.md
RUN cat > /home/user/scripts/README.md <<'EOF'
# Utility Scripts
This directory contains small helper scripts used in various automation tasks.
EOF

RUN chmod 0644 /home/user/scripts/README.md

# --- Empty directories ---------------------------------------
RUN mkdir -p /home/user/archives && \
    mkdir -p /home/user/logs && \
    chmod 0777 /home/user/archives && \
    chmod 0777 /home/user/logs

################################
# 3. Clean up APT caches        #
################################
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user