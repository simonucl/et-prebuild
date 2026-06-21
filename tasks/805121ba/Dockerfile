# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install required system packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create monitoring directory
RUN mkdir -p /home/user/monitoring

# check_disk.sh
RUN cat <<'EOF' > /home/user/monitoring/check_disk.sh
#!/usr/bin/env bash
echo "DISK OK"
EOF

# check_memory.sh
RUN cat <<'EOF' > /home/user/monitoring/check_memory.sh
#!/usr/bin/env bash
echo "MEMORY OK"
EOF

# Set permissions
RUN chmod 0755 /home/user/monitoring/check_disk.sh /home/user/monitoring/check_memory.sh && \
    chmod 0777 /home/user/monitoring && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:$PATH"

# Run script behavior
CMD ["bash", "-c", "exec \"$@\"", "bash"]

# Labels
LABEL Author="Monitoring-Makefile-Starter"
LABEL Description="Container preloaded with monitoring scripts and pytest."