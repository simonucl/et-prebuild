FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir pytest

# Prepare the initial exercise state
RUN mkdir -p /home/user/cloud-migration

RUN cat << 'EOF' > /home/user/cloud-migration/service.ini
[compute]
instance_type=t3.medium
region=us-east-1

[database]
engine=postgres
version=13
storage=100

[network]
cidr=10.0.0.0/16
ports=22,80,443
EOF

# Set permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/cloud-migration && \
    chmod 644 /home/user/cloud-migration/service.ini

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH