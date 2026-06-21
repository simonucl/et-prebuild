FROM ubuntu:22.04

# Basic tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure
RUN mkdir -p /home/user/configs

# config_20230115.conf
RUN cat <<'EOF' >/home/user/configs/config_20230115.conf
# Sample app config
  host = localhost
port=8080
max_connections = 100
# End
EOF

# config_20230410.conf
RUN cat <<'EOF' >/home/user/configs/config_20230410.conf
# Updated config
host = prod.example.com
port = 80
max_connections= 250
timeout = 30
EOF

# config_20230718.conf
RUN cat <<'EOF' >/home/user/configs/config_20230718.conf
## Production patch
host=prod.example.com
port=443
max_connections =300
timeout=45
enable_tls = true
#some comment
  cache_size= 512
EOF

# Permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/configs && \
    chmod 644 /home/user/configs/*.conf

# Environment variables
ENV PATH="$PATH:/home/user/.local/bin"

# Help / runscript equivalent
CMD echo "Container for configuration management task. No default run action."