FROM ubuntu:22.04

# Help text
# This container supplies the initial state for the “backup reference moment” exercise.
# It provides:
# • Python 3 and pytest
# • A writable /home/user directory
# No additional files are pre-created, so the learner can complete the task
# by issuing the required single command.

LABEL Author="Automated Build"
LABEL Description="Environment for the backup reference-moment task. Includes pytest and a writable /home/user directory."

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*