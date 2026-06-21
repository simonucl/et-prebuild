FROM ubuntu:22.04

# Install Python 3 and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state
RUN mkdir -p /home/user/configs && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/configs

# 1. Initial insecure ssh_app.yml
RUN cat > /home/user/configs/ssh_app.yml <<'EOF'
port: 22
permit_root_login: yes
password_authentication: yes
max_auth_tries: 6
EOF

# 2. Initial etcd_service.toml
RUN cat > /home/user/configs/etcd_service.toml <<'EOF'
[Service]
enable_debug = true
quota_backend_bytes = 0

[Security]
token = "simple"
client_cert_auth = false
EOF

RUN chmod 0666 /home/user/configs/ssh_app.yml /home/user/configs/etcd_service.toml

# Environment variables
RUN chmod 755 /home/user
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Default runscript behavior
CMD ["bash"]