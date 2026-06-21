# This image provides the initial environment for the “uptime summary” task.
# Python and pytest are pre-installed, and the required CSV file is placed in
# /home/user/logs/ with writable permissions so students can create the summary file.

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/logs && \
    chmod 0777 /home/user/logs && \
    chmod 755 /home/user

RUN cat << 'EOF' > /home/user/logs/uptime_full.csv
timestamp,status,response_ms
2023-05-01T00:00:00Z,UP,123
2023-05-01T00:05:00Z,UP,110
2023-05-01T00:10:00Z,DOWN,0
2023-05-01T00:15:00Z,UP,130
EOF

RUN chmod 0644 /home/user/logs/uptime_full.csv

CMD echo "Container for uptime summary exercise. Start an interactive shell to begin." && /bin/bash