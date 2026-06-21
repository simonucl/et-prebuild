FROM ubuntu:22.04

# Author YourName
# Description "Container for INI-file hardening task – initial state with config.ini and pytest installed"

# This container provides the starting environment for the INI hardening challenge.
# The file /home/user/appd/config.ini is pre-populated with the baseline content.
# Students must perform the required hardening steps when solving the exercise.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user || true && \
    mkdir -p /home/user/appd && \
    chown -R root:root /home/user && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/appd

RUN cat > /home/user/appd/config.ini <<'EOF'
[core]
enabled=true
secure=true
timeout=30

[analytics]
enabled=true
secure=false
sample_rate=10

[network]
enabled=true
secure=true
port=8080

[logging]
enabled=true
secure=false
level=debug

[beta]
enabled=true
secure=false
experimental=true
EOF

RUN chmod 0644 /home/user/appd/config.ini