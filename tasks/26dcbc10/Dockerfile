FROM ubuntu:22.04

# Labels
# Author: DevOpsTaskGen
# Description: Base image for “SECURITY ALERT” log-parsing challenge

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/devops

RUN cat > /home/user/devops/server.log <<'EOF'
2024-05-15 10:01:22 INFO User login succeeded: user=alice ip=192.168.1.10
2024-05-15 10:05:03 SECURITY ALERT Failed password attempt: user=root ip=203.0.113.45
2024-05-15 10:07:45 ERROR Database connection timeout
2024-05-15 10:12:11 SECURITY ALERT Multiple invalid login attempts: user=bob ip=198.51.100.23
2024-05-15 10:15:55 INFO Cron job finished
2024-05-15 10:17:20 SECURITY ALERT Failed password attempt: user=carol ip=203.0.113.45
2024-05-15 10:20:00 INFO Backup completed
EOF

RUN chmod 644 /home/user/devops/server.log && \
    chmod 777 /home/user/devops && \
    rm -f /home/user/devops/security_alerts.log /home/user/devops/blacklist.txt && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*