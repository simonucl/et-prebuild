FROM ubuntu:22.04

# Labels
LABEL Maintainer="edge-computing course autograder setup"
LABEL Description="Base image for the alpha321 error-log isolation assignment"

# Environment variables
ENV PYTHONUNBUFFERED=1

# Install Python tooling and pytest for the grader
RUN set -e && \
    apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the directory hierarchy for the raw log
RUN mkdir -p /home/user/deployment/logs

# Populate the raw log with the exact baseline content
RUN cat > /home/user/deployment/logs/raw_device.log <<'EOF'
[2023-08-12 14:03:22] [INFO]  DeviceID=alpha321 Temperature=23.4C
[2023-08-12 14:04:03] [WARN]  DeviceID=beta654  Battery=15%
[2023-08-12 14:05:10] [ERROR] DeviceID=alpha321 SensorFailure=Temp
[2023-08-12 14:05:46] [ERROR] DeviceID=gamma999 ConnectionLost
[2023-08-12 14:06:22] [INFO]  DeviceID=alpha321 Reconnected
[2023-08-12 14:07:00] [ERROR] DeviceID=alpha321 SensorFailure=Humidity
EOF

# Ensure permissive permissions so the non-root user can read the files
RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/deployment && \
    chmod 644 /home/user/deployment/logs/raw_device.log