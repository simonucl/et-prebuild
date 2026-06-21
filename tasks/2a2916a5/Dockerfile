FROM ubuntu:22.04

# Author automated_task_setup
# Description "Environment for log-processing automation task"

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        passwd && \
    pip3 install --no-cache-dir pytest

RUN set -eux && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user; \
    fi && \
    mkdir -p /home/user/logs

RUN cat <<'EOF' > /home/user/logs/app1.log
[2023-08-01 10:00:00] INFO Starting service
[2023-08-01 10:05:00] ERROR Failed to connect to database
[2023-08-01 10:06:00] WARN Cache miss
[2023-08-01 10:07:00] ERROR Timeout while reading from socket
[2023-08-01 10:08:00] INFO Service running
[2023-08-01 10:09:00] ERROR Failed to connect to database
EOF

RUN cat <<'EOF' > /home/user/logs/app2.log
[2023-08-01 09:00:00] INFO Booting
[2023-08-01 09:01:00] ERROR NullPointerException at line 42
[2023-08-01 09:02:00] ERROR NullPointerException at line 42
[2023-08-01 09:03:00] INFO Ready
EOF

RUN cat <<'EOF' > /home/user/logs/app3.log
[2023-08-01 11:00:00] INFO Starting cron
[2023-08-01 11:01:00] WARN Slow query
[2023-08-01 11:02:00] INFO Tick
EOF

RUN chmod -R a+rwX /home/user

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Container runscript equivalent
# echo "Container for log-processing task. Open a shell with: apptainer exec <image> /bin/bash"

RUN chmod 755 /home/user