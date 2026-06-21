# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN mkdir -p /home/user/logs && \
    chmod 0755 /home/user/logs

RUN echo "Sample uptime log for 2023-09-14" > /home/user/logs/uptime_2023-09-14_13-45-00.log && \
    echo "Sample uptime log for 2023-09-15" > /home/user/logs/uptime_2023-09-15_13-45-00.log

RUN rm -f /home/user/uptime_latest.log /home/user/uptime_link_check.txt || true

# Environment adjustments from %environment
RUN chmod 755 /home/user