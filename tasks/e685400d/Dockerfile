FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/deployment/firewall && \
    mkdir -p /home/user/deployment/logs

RUN cat > /home/user/deployment/firewall/iptables.rules <<'EOF'
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -p tcp --dport 22 -j ACCEPT
COMMIT
EOF

RUN chmod 666 /home/user/deployment/firewall/iptables.rules && \
    chmod 777 /home/user/deployment/firewall && \
    chmod 777 /home/user/deployment/logs && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8