FROM ubuntu:22.04

# Help section not provided in original file

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        tree && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/iot_gateway/logs

RUN cat > /home/user/iot_gateway/logs/device_events.log << 'EOF'
2023-10-11T14:00:01Z device-001 DATA_UPLOAD 110 200
2023-10-11T14:05:23Z device-002 DATA_UPLOAD 95 200
2023-10-11T14:12:47Z device-001 HEARTBEAT 30 200
2023-10-11T14:20:11Z device-003 DATA_UPLOAD 150 500
2023-10-11T14:45:00Z device-002 HEARTBEAT 28 200
2023-10-11T15:15:42Z device-001 DATA_UPLOAD 130 504
2023-10-11T15:40:17Z device-003 HEARTBEAT 32 200
2023-10-11T16:00:00Z device-004 DATA_UPLOAD 200 200
2023-10-11T16:10:05Z device-004 HEARTBEAT 33 404
2023-10-11T16:30:21Z device-002 DATA_UPLOAD 97 200
2023-10-11T16:35:00Z device-001 HEARTBEAT 29 200
2023-10-11T17:10:45Z device-003 DATA_UPLOAD 160 200
2023-10-11T17:20:35Z device-005 DATA_UPLOAD 180 502
2023-10-11T17:35:20Z device-005 HEARTBEAT 31 200
2023-10-11T17:45:50Z device-002 DATA_UPLOAD 101 503
EOF

RUN chmod -R a+rwx /home/user

RUN chmod 755 /home/user

ENV PYTHONIOENCODING=UTF-8