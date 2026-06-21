FROM ubuntu:22.04

# Author "Site-Admin Exercise Container"

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/site/logs

RUN cat > /home/user/site/logs/account_activity.log <<'EOF'
2023-08-01T09:00:01Z user=john ip=192.168.1.10 action=LOGIN status=OK
2023-08-01T09:05:43Z user=alice ip=203.0.113.17 action=LOGIN status=FAIL
2023-08-01T09:07:12Z user=bob ip=198.51.100.23 action=LOGIN status=FAIL
2023-08-01T09:11:58Z user=carol ip=10.0.0.5 action=LOGIN status=FAIL
2023-08-01T09:15:22Z user=dave ip=172.20.10.8 action=LOGIN status=FAIL
2023-08-01T09:20:30Z user=erin ip=203.0.113.17 action=LOGIN status=FAIL
2023-08-01T09:25:44Z user=frank ip=192.0.2.55 action=LOGIN status=OK
2023-08-01T09:30:01Z user=grace ip=198.51.100.23 action=LOGIN status=FAIL
2023-08-01T09:35:29Z user=heidi ip=192.168.1.15 action=LOGIN status=FAIL
EOF

RUN chmod 755 /home/user /home/user/site /home/user/site/logs && \
    chmod 644 /home/user/site/logs/account_activity.log