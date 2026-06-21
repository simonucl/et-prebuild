FROM ubuntu:22.04

# Labels
LABEL Author="IoT-Gateway-Task-Setup"
LABEL Description="Environment for IoT gateway critical-event extraction task"

# Environment variables
ENV PYTHONUNBUFFERED=1

# Install Python 3, pip, and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir pytest

# Create initial directory structure
RUN mkdir -p /home/user/iot_gateway/logs

# Create the log file with device events
RUN cat > /home/user/iot_gateway/logs/device_events.log <<'EOF'
2023-09-14T22:59:59Z [device-002] CRITICAL: Error code 0x0ABC: Unexpected shutdown
2023-09-15T00:00:01Z [device-004] INFO: Boot sequence initiated
2023-09-15T08:23:01Z [device-001] INFO: Temperature reading 22.5C
2023-09-15T10:00:00Z [device-003] WARNING: Battery low
2023-09-15T12:45:33Z [device-007] CRITICAL: Error code 0x0F4A: Sensor failure
2023-09-15T13:00:00Z [device-001] CRITICAL: Error code 0x00FF: Overheating detected
2023-09-15T15:15:15Z [device-001] CRITICAL: Error code 0x0100: Temperature threshold exceeded
2023-09-15T23:59:59Z [device-009] CRITICAL: Error code 0x0011: Network failure
2023-09-16T00:00:00Z [device-010] INFO: Boot sequence initiated
EOF

# Set permissive (but safe) permissions so the runtime
# non-root user can read the log and create sibling dirs
RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/iot_gateway && \
    chmod 644 /home/user/iot_gateway/logs/device_events.log

WORKDIR /home/user