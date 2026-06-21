FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Docker container for IoT staged deployment task with pytest pre-installed."

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Basic tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create initial directory tree under /home/user
RUN mkdir -p /home/user/iot_configs

# Create device_01 config
RUN mkdir -p /home/user/iot_configs/device_01 && \
    chmod 777 /home/user/iot_configs/device_01

RUN cat > /home/user/iot_configs/device_01/settings.conf <<EOF
# IoT Edge Device Config
DEVICE_ID=device_01
DEPLOY=NO
EOF

RUN chmod 666 /home/user/iot_configs/device_01/settings.conf

# Create device_02 config
RUN mkdir -p /home/user/iot_configs/device_02 && \
    chmod 777 /home/user/iot_configs/device_02

RUN cat > /home/user/iot_configs/device_02/settings.conf <<EOF
# IoT Edge Device Config
DEVICE_ID=device_02
DEPLOY=NO
EOF

RUN chmod 666 /home/user/iot_configs/device_02/settings.conf

# Create device_03 config
RUN mkdir -p /home/user/iot_configs/device_03 && \
    chmod 777 /home/user/iot_configs/device_03

RUN cat > /home/user/iot_configs/device_03/settings.conf <<EOF
# IoT Edge Device Config
DEVICE_ID=device_03
DEPLOY=NO
EOF

RUN chmod 666 /home/user/iot_configs/device_03/settings.conf

# Create device_04 config
RUN mkdir -p /home/user/iot_configs/device_04 && \
    chmod 777 /home/user/iot_configs/device_04

RUN cat > /home/user/iot_configs/device_04/settings.conf <<EOF
# IoT Edge Device Config
DEVICE_ID=device_04
DEPLOY=NO
EOF

RUN chmod 666 /home/user/iot_configs/device_04/settings.conf

# Create device_05 config
RUN mkdir -p /home/user/iot_configs/device_05 && \
    chmod 777 /home/user/iot_configs/device_05

RUN cat > /home/user/iot_configs/device_05/settings.conf <<EOF
# IoT Edge Device Config
DEVICE_ID=device_05
DEPLOY=NO
EOF

RUN chmod 666 /home/user/iot_configs/device_05/settings.conf

# Firmware directory
RUN mkdir -p /home/user/new_firmware && \
    touch /home/user/new_firmware/device_01.bin && \
    touch /home/user/new_firmware/device_02.bin && \
    touch /home/user/new_firmware/device_04.bin && \
    touch /home/user/new_firmware/device_05.bin

RUN cat > /home/user/new_firmware/device_01.md5 <<EOF
3e25960a79dbc69b674cd4ec67a72c62  device_01.bin
EOF

RUN cat > /home/user/new_firmware/device_02.md5 <<EOF
8f14e45fceea167a5a36dedd4bea2543  device_02.bin
EOF

RUN cat > /home/user/new_firmware/device_04.md5 <<EOF
1679091c5a880faf6fb5e6087eb1b2dc  device_04.bin
EOF

RUN cat > /home/user/new_firmware/device_05.md5 <<EOF
d3d9446802a44259755d38e6d163e820  device_05.bin
EOF

RUN chmod 777 /home/user/new_firmware && \
    chmod 666 /home/user/new_firmware/*.bin && \
    chmod 666 /home/user/new_firmware/*.md5

# Old backups directory
RUN mkdir -p /home/user/old_backups && \
    echo "legacy backup 1" > /home/user/old_backups/stale1.bak && \
    echo "legacy backup 2" > /home/user/old_backups/stale2.bak && \
    echo "Some human-readable notes." > /home/user/old_backups/notes.txt && \
    chmod 777 /home/user/old_backups && \
    chmod 666 /home/user/old_backups/stale1.bak && \
    chmod 666 /home/user/old_backups/stale2.bak && \
    chmod 666 /home/user/old_backups/notes.txt

# Ensure deployment report does not yet exist
RUN rm -f /home/user/deployment_report.log

# Set home directory permissions
RUN chmod 755 /home/user

WORKDIR /home/user