FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    python3 -m pip install --no-cache-dir pytest

# Prepare initial workspace
RUN mkdir -p /home/user/project/api_service

# Create pristine config.ini
RUN cat > /home/user/project/api_service/config.ini <<'EOF'
[Database]
host=localhost
port=5432
user=dbuser
password=secret

[API]
base_url=https://api.example.com
timeout=30
retries=3

[Caching]
enabled=true
ttl=600
EOF

# Permissions
RUN chmod -R a+rwX /home/user/project && \
    chmod 755 /home/user

# Environment variables
ENV PATH="$PATH:~/.local/bin"

CMD ["bash"]