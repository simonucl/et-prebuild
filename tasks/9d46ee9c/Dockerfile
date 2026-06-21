# This Docker image provides the initial filesystem state for the ERROR-count task.
# Three log files are placed under /home/user/project/logs/, and pytest is installed for automated grading.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/logs

RUN cat > /home/user/project/logs/app.log <<'EOF'
INFO Application started
WARN Cache miss
ERROR Failed to load config
INFO Shutdown complete
EOF

RUN cat > /home/user/project/logs/db.log <<'EOF'
INFO Connection established
ERROR Query timeout
ERROR Could not commit
INFO Connection closed
EOF

RUN cat > /home/user/project/logs/auth.log <<'EOF'
INFO User login
WARN Password attempt
ERROR Invalid token
ERROR Session expired
ERROR Permission denied
INFO Logout
EOF

RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/project && \
    chmod 644 /home/user/project/logs/*.log

CMD echo "Container for ERROR line–count task. Use an interactive shell:" && \
    echo "  docker run -it <image> /bin/bash"