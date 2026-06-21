FROM ubuntu:22.04

# Help text
# This container image provides the initial environment for the
# “legacy utility” task. Pytest is installed, and the directory
# /home/user/legacy_utils contains the non-executable script greet.sh
# that the learner must run and log according to the assignment.

LABEL Author="Legacy-Utility Setup"

ENV HOME=/home/user

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 1777 /home/user && \
    mkdir -p /home/user/legacy_utils

RUN cat << 'EOF' > /home/user/legacy_utils/greet.sh
#!/bin/bash
echo "greet.sh version 1.0"
echo "Hello, $1!"
EOF

RUN chmod 0644 /home/user/legacy_utils/greet.sh