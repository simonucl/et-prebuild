# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create directories
RUN mkdir -p /home/user/iot_logs

# device01.log
RUN cat <<'EOF' > /home/user/iot_logs/device01.log
[2023-07-20 12:00:00] INFO  Sensor reading: 23.4
[2023-07-20 12:01:00] ERROR SENSOR_TIMEOUT E105 Connection lost
[2023-07-20 12:02:00] WARN  Retry attempt
[2023-07-20 12:03:00] ERROR LOW_BATTERY E201 Battery level 5%
[2023-07-20 12:04:00] INFO  Sensor reading: 24.1
EOF

# device02.log
RUN cat <<'EOF' > /home/user/iot_logs/device02.log
[2023-07-20 12:10:00] INFO  Boot
[2023-07-20 12:11:00] ERROR SENSOR_TIMEOUT E105 Connection lost
[2023-07-20 12:12:00] ERROR OVERHEAT E301 Temperature 85C
[2023-07-20 12:13:00] ERROR SENSOR_TIMEOUT E105 Connection lost
[2023-07-20 12:14:00] INFO  Sensor reading: 22
EOF

# device03.log
RUN cat <<'EOF' > /home/user/iot_logs/device03.log
[2023-07-20 12:20:00] ERROR LOW_BATTERY E201 Battery level 4%
[2023-07-20 12:21:00] ERROR OVERHEAT E301 Temperature 87C
[2023-07-20 12:22:00] WARN  Retry
[2023-07-20 12:23:00] ERROR LOW_BATTERY E201 Battery level 3%
EOF

# Permissions and ownership
RUN chmod 755 /home/user && \
    chmod 0644 /home/user/iot_logs/*.log && \
    chown -R 1000:1000 /home/user || true

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Help comments
# Container for the IoT-logs exercise.
# Run your commands inside the container as needed.

CMD echo "Container for the IoT-logs exercise." && \
    echo "Run your commands inside the container as needed."