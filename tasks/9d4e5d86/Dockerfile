FROM ubuntu:22.04

# Help text from %help section
# This image contains:
#   - /home/user/project with a sample.txt file
#   - NO /home/user/backup directory yet (must be created by the learner)
# Pytest is installed so the automated grader can run its tests.

LABEL Author="backup-proof-of-concept-preparer"
LABEL Description="Container providing initial state for backup PoC exercise"

ENV HOME=/home/user

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project && \
    echo "Sample content for the monitoring-platform backup proof-of-concept." > /home/user/project/sample.txt && \
    chmod 0777 /home/user && \
    chmod -R a+rX /home/user/project && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*