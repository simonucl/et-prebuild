FROM ubuntu:22.04

# Help text
# This container image provides the starting point for the “Container Error
# Analysis” exercise. Three days of raw logs are located in:
#     /home/user/container_logs/
# The directory /home/user/analysis/ does NOT exist yet and must be created
# by the learner. Pytest is installed so the automated grading harness can
# validate the initial state.

LABEL Author="Log-Analysis Exercise Maintainer"
LABEL Version="1.0"
LABEL Description="Initial state for Docker-log analysis exercise"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -e && \
    if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user || true && \
        useradd -m -u 1000 -g 1000 -s /bin/bash user || true ; \
    fi

RUN mkdir -p /home/user/container_logs

RUN cat >/home/user/container_logs/app_2024-06-01.log <<'EOF'
2024-06-01T10:15:03Z 4a1b2c3d4e5f INFO Container started
2024-06-01T10:15:05Z 4a1b2c3d4e5f INFO Health check passed
2024-06-01T12:05:47Z 4a1b2c3d4e5f ERROR Connection timeout to database
2024-06-01T12:10:03Z ab12cd34ef56 INFO Container started
2024-06-01T12:15:47Z ab12cd34ef56 ERROR Connection timeout to database
2024-06-01T13:20:10Z 7890abcd1234 INFO Container started
2024-06-01T13:25:22Z 7890abcd1234 ERROR Unexpected EOF while reading response
EOF

RUN cat >/home/user/container_logs/app_2024-06-02.log <<'EOF'
2024-06-02T09:00:00Z 4a1b2c3d4e5f INFO Daily scheduled task started
2024-06-02T09:05:00Z 4a1b2c3d4e5f ERROR Failed to pull image
2024-06-02T11:45:15Z ab12cd34ef56 WARN Memory usage high
2024-06-02T12:00:03Z 4a1b2c3d4e5f ERROR Connection timeout to database
2024-06-02T14:30:42Z 7890abcd1234 ERROR Connection timeout to database
EOF

RUN cat >/home/user/container_logs/app_2024-06-03.log <<'EOF'
2024-06-03T08:10:11Z ab12cd34ef56 INFO Health check passed
2024-06-03T10:22:47Z ab12cd34ef56 ERROR Failed to pull image
2024-06-03T11:00:00Z 4a1b2c3d4e5f ERROR Connection timeout to database
2024-06-03T12:15:17Z 7890abcd1234 ERROR Unexpected EOF while reading response
2024-06-03T15:45:55Z 7890abcd1234 ERROR Connection timeout to database
EOF

RUN chmod -R a+r /home/user/container_logs && \
    chmod a+rwx /home/user