FROM ubuntu:22.04

# Help:
# This container provides the initial state for the backup creation task.
# Pytest is pre-installed, and /home/user/app contains the two source files
# (index.html and config.yaml). The /home/user/backups directory is intentionally
# absent so the agent can create it during the exercise.

LABEL Author="task-preparer"
LABEL Description="Environment for backup-creation task"

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/app && \
    printf '<html>Hello World</html>\n' > /home/user/app/index.html && \
    printf 'port: 8080\n' > /home/user/app/config.yaml && \
    chmod -R a+rwX /home/user