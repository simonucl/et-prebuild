FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    mkdir -p /home/user/firewall && \
    chmod 0700 /home/user/firewall

RUN cat > /home/user/firewall/current_rules.v4 <<'EOF'
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT  -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A INPUT  -p icmp -j ACCEPT
-A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A FORWARD -s 10.10.10.0/24   -p tcp -m tcp --dport 22  -j ACCEPT
-A FORWARD -j DROP
COMMIT
EOF

RUN chmod 0600 /home/user/firewall/current_rules.v4 && \
    chmod 755 /home/user

ENV HOME=/home/user

CMD ["/bin/bash"]