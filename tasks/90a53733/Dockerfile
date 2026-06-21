# Author="ChatGPT - Apptainer setup"
# Description="Container for the task: Generate an error–frequency summary from an application log"
# Help:
# This container image provides the initial environment for the
# "Generate an error–frequency summary from an application log" task.
# It contains:
#   • /home/user/dev_project/logs/server.log  (source log file)
#   • Python 3 with pytest pre-installed for automated grading.
# The student must create /home/user/dev_project/logs/error_summary.log
# according to the task description.

FROM ubuntu:22.04

RUN set -e && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/dev_project/logs

RUN cat <<'EOF' > /home/user/dev_project/logs/server.log
2024-05-10 10:00:01 [INFO] Server started
2024-05-10 10:05:12 [ERROR] [E1001] Failed to connect to database
2024-05-10 10:06:05 [WARN] Low disk space
2024-05-10 10:07:45 [ERROR] [E2345] Timeout while processing request
2024-05-10 10:08:30 [ERROR] [E1001] Failed to connect to database
2024-05-10 10:09:01 [INFO] User login successful
2024-05-10 10:10:15 [ERROR] [E7777] Null pointer exception
2024-05-10 10:15:00 [INFO] Cache cleared
2024-05-10 10:20:22 [ERROR] [E2345] Timeout while processing request
2024-05-10 10:25:33 [INFO] Session terminated
EOF

RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/dev_project && \
    chmod 644 /home/user/dev_project/logs/server.log