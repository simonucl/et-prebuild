FROM ubuntu:22.04

# Install Python/pip and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial workspace expected by the automated tests
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Create ServerA log
RUN cat > /home/user/serverA.log <<'EOF'
2023-08-01 12:00:01 INFO Service started
2023-08-01 12:10:15 ERROR Connection timeout
2023-08-01 12:11:00 INFO Reconnected
2023-08-01 12:20:05 ERROR Disk full
2023-08-01 12:30:00 WARNING High memory usage
EOF

RUN chmod 0644 /home/user/serverA.log

# Create ServerB log
RUN cat > /home/user/serverB.log <<'EOF'
2023-08-01 12:05:00 INFO Service started
2023-08-01 12:15:45 ERROR Connection refused
2023-08-01 12:16:30 ERROR Connection refused
2023-08-01 12:18:20 INFO Reconnected
2023-08-01 12:25:55 ERROR Disk full
EOF

RUN chmod 0644 /home/user/serverB.log

# Set environment variables
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:$PATH"

WORKDIR /home/user