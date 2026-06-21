# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Set up initial dashboard directory and files
RUN mkdir -p /home/user/dashboards/new

# Create single-line JSON files
RUN printf '{"title":"Database Metrics","uid":"TEMP-db789","tags":["database"]}' \
        > /home/user/dashboards/new/db_metrics.json && \
    printf '{"title":"Queue Depth","uid":"TEMP-queue456","tags":["queues"]}' \
        > /home/user/dashboards/new/queue_depth.json && \
    printf '{"title":"System Overview","uid":"TEMP-abc123","tags":["system"]}' \
        > /home/user/dashboards/new/system_overview.json

# Permissions
RUN chmod 777 /home/user /home/user/dashboards /home/user/dashboards/new && \
    chmod 666 /home/user/dashboards/new/*.json && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:$PATH"