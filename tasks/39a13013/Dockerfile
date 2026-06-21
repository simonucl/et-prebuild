FROM ubuntu:22.04

# Author: rotating-credentials-task
# Container for the “rotate INI credentials” task.
# Provides the initial credentials.ini file and has pytest installed
# so that the automated grader can run its checks.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/app/config

RUN cat >/home/user/app/config/credentials.ini <<'EOF'
[default]
access_key = AKIAEXAMPLE123456
secret_key = OLDSECRET_987654321==
version = 7
EOF

RUN chmod -R 0777 /home/user/app && \
    chmod 755 /home/user