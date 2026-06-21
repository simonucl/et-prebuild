FROM ubuntu:22.04

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash && \
    pip3 install --no-cache-dir pytest

# Create unprivileged user 'user' with home directory /home/user
RUN if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g user -s /bin/bash user; \
    fi

# Prepare initial project workspace and template file
RUN su - user -c 'mkdir -p /home/user/projects/iot_gateway'

RUN cat > /home/user/projects/iot_gateway/config.template.env <<'EOF'
EDGE_DEVICE_ID=<DEV_ID>
MQTT_BROKER_HOST=<BROKER_HOST>
MQTT_BROKER_PORT=<BROKER_PORT>
SENSOR_POLL_INTERVAL=<POLL_INT>
FIRMWARE_VERSION=<FW_VER>
EOF

# Ensure ~/.bashrc exists (without the firmware export line)
RUN if [ ! -f /home/user/.bashrc ]; then \
        touch /home/user/.bashrc; \
    fi

# Ownership: everything in /home/user belongs to the 'user' account
RUN chown -R user:user /home/user && \
    chmod 755 /home/user

CMD ["/bin/bash"]