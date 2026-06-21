# Converted from Apptainer definition file
FROM ubuntu:22.04

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

# Install packages and pytest
RUN set -e && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/iot_configs && \
    chmod 755 /home/user && \
    chmod 755 /home/user/iot_configs

# Create device_alpha.ini
RUN cat >/home/user/iot_configs/device_alpha.ini <<'EOF'
[Network]
ip = 192.168.10.11
location = RoofTop

[Sensors]
enabled = temp,humidity,pressure

[System]
os = TinyLinux
last_maintained = 2023-05-10
EOF

# Create device_beta.ini
RUN cat >/home/user/iot_configs/device_beta.ini <<'EOF'
[Network]
ip = 192.168.10.12
location = Warehouse55

[Sensors]
enabled = temp,vibration

[System]
os = TinyLinux
last_maintained = 2023-04-01
EOF

# Create device_gamma.ini
RUN cat >/home/user/iot_configs/device_gamma.ini <<'EOF'
[Network]
ip = 192.168.10.13
location = Dock

[Sensors]
enabled = temp,humidity,air_quality,co2

[System]
os = TinyLinux
last_maintained = 2022-12-15
EOF

# Set permissions
RUN chmod 644 /home/user/iot_configs/device_*.ini

# Final message equivalent
RUN echo "Initial container setup complete."