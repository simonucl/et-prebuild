FROM ubuntu:22.04

# Author: AI-generated
# Description: Base image for “Synchronize Remote Log Files” coding task

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash user

RUN mkdir -p /home/user/remote_logs && \
    mkdir -p /home/user/central_logs

RUN cat > /home/user/remote_logs/app1_20230910.log <<'EOF'
2023-09-10 08:00:01 INFO Startup complete
2023-09-10 08:05:14 ERROR Failed to connect to database
2023-09-10 08:07:55 INFO Retrying connection
2023-09-10 08:08:02 ERROR Database connection timeout
2023-09-10 08:09:10 INFO Shutdown initiated
EOF

RUN cat > /home/user/remote_logs/app2_20230910.log <<'EOF'
2023-09-10 09:00:00 INFO Service started
2023-09-10 09:15:22 WARN High memory usage
2023-09-10 09:20:37 ERROR Out of memory
2023-09-10 09:21:00 ERROR Could not allocate buffer
2023-09-10 09:22:45 INFO Service restarted
EOF

RUN cat > /home/user/central_logs/app1_20230909.log <<'EOF'
2023-09-09 07:59:59 INFO Previous day startup
2023-09-09 08:10:10 ERROR Sample error
2023-09-09 08:20:20 INFO Shutdown
EOF

RUN chown -R user:user /home/user && \
    chmod a+rX /home/user && \
    chmod -R a+r /home/user/remote_logs && \
    chmod -R a+rwX /home/user/central_logs

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=utf-8

RUN chmod 755 /home/user

CMD echo "Container for log-analysis task ready. Launch your solution inside."