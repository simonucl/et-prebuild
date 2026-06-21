FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest pytest-order

# Create project directory
RUN mkdir -p /home/user/dns_profile

# Create starter file with custom hosts
RUN cat > /home/user/dns_profile/custom_hosts <<'EOF'
192.168.50.10 app.internal.local app
192.168.50.11 db.internal.local db
192.168.50.12 cache.internal.local cache
EOF

# Correct permissions
RUN chmod 0755 /home/user/dns_profile && \
    chmod 0644 /home/user/dns_profile/custom_hosts

# Clean up APT cache to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/bin:$PATH

# Set home directory permissions
RUN chmod 755 /home/user

# Labels
LABEL Author="Auto-generated for hostname resolution task"
LABEL Description="Container providing starter environment and pytest for the task: Profile and document local hostname resolution."

WORKDIR /home/user

CMD ["/bin/bash"]