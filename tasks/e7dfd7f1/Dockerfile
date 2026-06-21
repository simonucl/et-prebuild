FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/sim_logs && \
    chmod 0755 /home/user /home/user/sim_logs || true

RUN cat > /home/user/sim_logs/apt_history.log <<'EOF'
Start-Date: 2024-04-15  09:21:07
Commandline: apt-get install nginx
Install: nginx:amd64 (1.18.0-6ubuntu14.3, automatic)
End-Date: 2024-04-15  09:21:09
Start-Date: 2024-04-15  09:22:45
Commandline: apt-get upgrade
E: Sub-process /usr/bin/dpkg returned an error code (1)
Err:1 http://archive.ubuntu.com/ubuntu focal-updates/main amd64 libc6 amd64 2.31-0ubuntu9.9
Fetched 0 B in 3s (0 B/s)
End-Date: 2024-04-15  09:22:48
EOF

RUN chmod 0644 /home/user/sim_logs/apt_history.log

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8