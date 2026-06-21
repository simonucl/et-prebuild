FROM ubuntu:22.04

# Help text
# This container provides the initial state for the “cleaning log” task.
# It contains:
# • /home/user/project/cleaning.log with the required 8 log lines.
# • pytest installed for automated checking.

LABEL Author="Your Name <you@example.com>"
LABEL Description="Environment for the cleaning log analysis exercise"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project && \
    chmod 0777 /home/user/project

RUN cat >/home/user/project/cleaning.log <<'EOF'
2023-09-01 09:15:21,123 INFO Removed duplicate row id=3
2023-09-01 09:15:22,456 INFO Replaced null price in row id=2 with mean=1.07
2023-09-01 09:15:23,789 INFO Replaced null quantity in row id=4 with mean=8.25
2023-09-01 09:15:24,012 INFO Replaced null price in row id=5 with mean=1.07
2023-09-01 09:15:25,345 INFO Removed duplicate row id=7
2023-09-01 09:15:26,678 INFO Replaced null price in row id=8 with mean=1.07
2023-09-01 09:15:27,901 INFO Replaced null quantity in row id=9 with mean=8.25
2023-09-01 09:15:29,234 INFO Replaced null quantity in row id=10 with mean=8.25
EOF

RUN chmod 0644 /home/user/project/cleaning.log