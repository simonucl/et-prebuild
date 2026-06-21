FROM ubuntu:22.04

# Install Python and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial filesystem state
RUN mkdir -p /home/user/iot_devices

# Create inventory CSV with exact contents
RUN cat > /home/user/iot_devices/device_registry.csv <<'EOF'
device_id,mac_addr,location,firmware
dev-001,AA:BB:CC:DD:EE:01,warehouse,1.2.3
dev-002,AA:BB:CC:DD:EE:02,warehouse,1.2.2
dev-003,AA:BB:CC:DD:EE:03,retail_store,1.2.3
dev-004,AA:BB:CC:DD:EE:04,office,1.2.1
dev-005,AA:BB:CC:DD:EE:05,office,1.2.3
EOF

# Permissions
RUN chmod -R a+rwX /home/user

# Metadata from %labels
# Author: OTA-exercise container setup
# Description: Provides initial state and pytest for the edge-computing OTA task.

# Default command from %runscript
CMD echo "Container for OTA-update exercise." && \
    echo "Use this shell to work on the task." && \
    exec /bin/bash "$@"