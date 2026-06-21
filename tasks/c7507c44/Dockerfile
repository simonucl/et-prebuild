# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure home directory exists
RUN mkdir -p /home/user

# Seed raw-data directory and create placeholder CSV files
RUN mkdir -p /home/user/data/raw

RUN cat > /home/user/data/raw/cats_vs_dogs.csv <<'EOF'
id,feature,label
1,sample_data,cat
2,another_sample,dog
EOF

RUN cat > /home/user/data/raw/flowers102.csv <<'EOF'
id,feature,category
1,sample_data,rose
2,another_sample,lily
EOF

RUN cat > /home/user/data/raw/cifar10.csv <<'EOF'
id,feature,label
1,sample_data,airplane
2,another_sample,ship
EOF

# Permissions
RUN chmod -R a+rX /home/user && chmod 755 /home/user

LABEL Author="Your Name"
LABEL Description="Base image for configuration files task — provides raw CSV data and pytest."