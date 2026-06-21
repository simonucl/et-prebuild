# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer %labels
LABEL Author="FinOps Exercise Container"
LABEL Description="Environment for the FinOps cost report archiving exercise."

# Install system dependencies, Python, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        build-essential && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user `user` with UID/GID 1000 and home directory /home/user
RUN set -eux && \
    groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# Prepare the initial exercise file in the user's home directory
RUN set -eux && \
    mkdir -p /home/user && \
    cat > /home/user/cost_report_june_2023.csv <<'EOF'
Service,Resource,Cost
EC2,i-1234567890abcdef0,123.45
S3,my-bucket,10.00
EOF

# Ensure ownership and sane permissions
RUN set -eux && \
    chown -R 1000:1000 /home/user && \
    chmod 644 /home/user/cost_report_june_2023.csv && \
    chmod 755 /home/user

# Environment variables from Apptainer %environment
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Switch to non-root user
USER user
WORKDIR /home/user