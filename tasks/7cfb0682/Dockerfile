FROM ubuntu:22.04

# Help / metadata from %help and %labels
LABEL Author="IoT-Firmware-Challenge"
LABEL Description="Container with initial state for IoT firmware deployment exercise."
LABEL Version="v1.0"

ENV PYTHONIOENCODING=UTF-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gawk \
        sed \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/iot_configs

RUN cat <<'EOF' >/home/user/iot_configs/dev01.cfg
device_id=dev01
ip=192.168.1.101
status=online
firmware_version=1.0.2
EOF

RUN cat <<'EOF' >/home/user/iot_configs/dev02.cfg
device_id=dev02
ip=192.168.1.102
status=offline
firmware_version=1.0.2
EOF

RUN cat <<'EOF' >/home/user/iot_configs/dev03.cfg
device_id=dev03
ip=192.168.1.103
status=online
firmware_version=1.0.1
EOF

RUN chmod -R a+rwx /home/user
RUN chmod 755 /home/user

CMD echo "This is a build container for the IoT firmware-update task." && \
    echo "Execute your own scripts/tests inside the container as needed."