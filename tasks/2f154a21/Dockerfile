FROM ubuntu:22.04

# Author tinyftp-initial-state
LABEL Author="tinyftp-initial-state"

ENV PYTHONIOENCODING=UTF-8
ENV HOME=/home/user

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/tinyftp && \
    mkdir -p /home/user/logs

RUN cat <<'EOF' > /home/user/tinyftp/tinyftp.conf
# tinyftp configuration
port=2121
log-level=INFO
EOF

RUN cat <<'EOF' > /home/user/logs/tinyftp.log
2023-09-01 12:00:00 INFO: Server started on port 2121
2023-09-01 12:01:00 DEBUG: Connection from 192.168.1.10 accepted
2023-09-01 12:02:00 ERROR: Failed login attempt for user 'john'
2023-09-01 12:03:00 DEBUG: Connection closed for 192.168.1.10
2023-09-01 12:04:00 INFO: Server status: OK
EOF

RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user