FROM ubuntu:22.04

# Author temperature-telemetry-setup
# Description "Environment for temperature telemetry parsing exercise"

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/logs

RUN cat > /home/user/logs/device_telemetry_2024-06-01.log <<'EOF'
2024-06-01T10:00:00Z device_id=101 TEMP=69.0C VOLT=3.6
2024-06-01T10:05:00Z device_id=102 TEMP=71.2C VOLT=3.6
2024-06-01T10:10:00Z device_id=103 TEMP=66.5C VOLT=3.7
2024-06-01T10:15:00Z device_id=104 TEMP=75.8C VOLT=3.5
2024-06-01T10:20:00Z device_id=105 TEMP=70.0C VOLT=3.8
2024-06-01T10:25:00Z device_id=106 TEMP=80.1C VOLT=3.6
EOF

RUN chmod 644 /home/user/logs/device_telemetry_2024-06-01.log && \
    chmod 755 /home/user /home/user/logs

RUN rm -rf /home/user/output || true