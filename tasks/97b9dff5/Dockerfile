FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir --upgrade pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user 'user'
RUN useradd -m -s /bin/bash user

# Build initial filesystem state
RUN mkdir -p /home/user/network_configs

# router.yml
RUN cat << 'EOF' > /home/user/network_configs/router.yml
network:
  interfaces:
    - name: eth0
      address: 192.168.1.1/24
  dns:
    - 1.1.1.1
    - 9.9.9.9
EOF

# firewall.toml
RUN cat << 'EOF' > /home/user/network_configs/firewall.toml
[default]
policy = "deny"

[[rule]]
action = "allow"
port = 22
protocol = "tcp"

[[rule]]
action = "allow"
port = 80
protocol = "tcp"
EOF

# Permissions
RUN chmod 0755 /home/user/network_configs && \
    chmod 0644 /home/user/network_configs/router.yml /home/user/network_configs/firewall.toml && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

# Default runscript behavior
CMD ["bash"]