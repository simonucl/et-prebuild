FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create home and log directories with permissions
RUN mkdir -p /home/user/server_logs && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/server_logs

# Create web01.log
RUN cat > /home/user/server_logs/web01.log <<'EOF'
2023-06-01 00:00:01 status=UP
2023-06-01 01:00:01 status=UP
2023-06-01 02:00:01 status=UP
2023-06-01 03:00:01 status=UP
2023-06-01 04:00:01 status=UP
2023-06-01 05:00:01 status=UP
2023-06-01 06:00:01 status=UP
2023-06-01 07:00:01 status=DOWN
2023-06-01 08:00:01 status=DOWN
2023-06-01 09:00:01 status=DOWN
EOF

# Create db01.log
RUN cat > /home/user/server_logs/db01.log <<'EOF'
2023-06-01 00:30:01 status=UP
2023-06-01 01:30:01 status=UP
2023-06-01 02:30:01 status=UP
2023-06-01 03:30:01 status=UP
2023-06-01 04:30:01 status=UP
2023-06-01 05:30:01 status=DOWN
2023-06-01 06:30:01 status=DOWN
2023-06-01 07:30:01 status=DOWN
2023-06-01 08:30:01 status=DOWN
2023-06-01 09:30:01 status=DOWN
EOF

# Set permissions on log files
RUN chmod 0644 /home/user/server_logs/*.log && \
    chmod 755 /home/user

# Labels
LABEL Author="task-prep-script"
LABEL Description="Environment for heartbeat log summary task – includes pytest and initial log files."