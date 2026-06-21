FROM ubuntu:22.04

# Labels
LABEL Author="On-call Ops Automation"
LABEL Description="Baseline image for the \"inventory-app\" incident-response task"

# Install Python tooling required by the automated test suite
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the directory structure for the incident-response task
RUN mkdir -p /home/user/services/inventory-app/config && \
    mkdir -p /home/user/services/inventory-app/runtime && \
    mkdir -p /home/user/incident_logs

# Ensure directory permissions are exactly 0755
RUN chmod 0755 /home/user \
               /home/user/services \
               /home/user/services/inventory-app \
               /home/user/services/inventory-app/config \
               /home/user/services/inventory-app/runtime \
               /home/user/incident_logs

# Populate configuration file
RUN cat > /home/user/services/inventory-app/config/env.conf <<'EOF'
APP_ENV=production
PORT=4000
EOF

# Create service status file
RUN echo "running on 4000" > /home/user/services/inventory-app/runtime/service.status

# Create the mock service helper script
RUN cat > /home/user/services/inventory-app/mock_service.sh <<'EOSH'
#!/usr/bin/env bash
# very small helper: writes to service.status
set -e
RUNTIME_DIR="$(dirname "$0")/runtime"
STATUS_FILE="${RUNTIME_DIR}/service.status"
CONFIG_FILE="$(dirname "$0")/config/env.conf"

if [[ "$1" == "start" ]]; then
    source "${CONFIG_FILE}"
    echo "running on ${PORT}" > "${STATUS_FILE}"
elif [[ "$1" == "stop" ]]; then
    echo "stopped" > "${STATUS_FILE}"
else
    echo "Usage: $0 {start|stop}"
    exit 1
fi
EOSH

# Set correct permissions for files
RUN chmod 0755 /home/user/services/inventory-app/mock_service.sh && \
    chmod 0644 /home/user/services/inventory-app/config/env.conf && \
    chmod 0644 /home/user/services/inventory-app/runtime/service.status

# Guarantee a trailing newline in service.status (safety)
RUN sed -i -e '$a\' /home/user/services/inventory-app/runtime/service.status

# Environment variables
ENV PATH="${PATH}:/home/user/services/inventory-app"

WORKDIR /home/user