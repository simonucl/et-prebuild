# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install system dependencies and Python tooling
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        locales \
        ca-certificates && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Create the initial directory structure and seed CSV data files
# ------------------------------------------------------------------
RUN mkdir -p /home/user/datasets

RUN cat > /home/user/datasets/species_A.csv << 'EOF'
id,name,weight,length
1,Panthera leo,190,2.0
2,Panthera pardus,,1.5
3,,120,1.1
4,Panthera tigris,220,2.3
5,Acinonyx jubatus,72,
EOF

RUN cat > /home/user/datasets/species_B.csv << 'EOF'
id,name,weight,length
6,Canis lupus,45,1.3
7,Canis latrans,15,0.9
8,,33,1.0
9,Canis aureus,,1.1
EOF

# Ensure non-root container users have full read/write access
RUN chmod -R a+rwx /home/user/datasets

# Optionally create a matching user entry
RUN useradd -m -u 1000 -s /bin/bash user || true

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# Clean up package lists to keep the image small
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Environment variables (from %environment)
# ------------------------------------------------------------------
ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PYTHONUNBUFFERED=1