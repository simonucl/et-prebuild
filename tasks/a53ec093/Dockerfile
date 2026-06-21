FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/device_configs/site_a && \
    mkdir -p /home/user/device_configs/site_b

# site_a/gateway.cfg
RUN cat >/home/user/device_configs/site_a/gateway.cfg <<'EOF'
gateway_id=GW-001
ip_address=192.168.1.1
port=1883
EOF

# site_a/sensor1.cfg
RUN cat >/home/user/device_configs/site_a/sensor1.cfg <<'EOF'
sensor_id=S-100
frequency=30
unit=celsius
EOF

# site_b/sensor2.cfg
RUN cat >/home/user/device_configs/site_b/sensor2.cfg <<'EOF'
sensor_id=S-200
frequency=15
unit=humidity
EOF

# Ensure all users can read/write the workspace
RUN chmod -R a+rwX /home/user

LABEL Maintainer="edge-computing-task-preparer"