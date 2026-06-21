FROM ubuntu:22.04

# Labels
LABEL Author="edge-engineering-prep"
LABEL Description="Container for IoT gateway diagnostic-bundle exercise (pytest included)."

# Base tools and Python environment
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip python3-setuptools python3-dev \
        iputils-ping net-tools procps \
        ca-certificates curl && \
    pip3 install --no-cache-dir pytest

# Create non-privileged user and required directory layout
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi

# Prepare deployment directory
RUN mkdir -p /home/user/iot_deployment

# Create devices.txt file
RUN cat > /home/user/iot_deployment/devices.txt <<'EOF'
127.0.0.1
192.0.2.1
EOF

# Set permissions
RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/iot_deployment && \
    chmod 0644 /home/user/iot_deployment/devices.txt && \
    chown -R user:user /home/user

# Clean up APT caches to shrink image
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]