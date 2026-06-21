FROM ubuntu:22.04

# Author "OpenAI Assistant"
# Description "Environment for SSH firewall audit task with pytest installed"

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/firewall

RUN cat > /home/user/firewall/iptables.rules <<'EOF'
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
COMMIT
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/firewall && \
    chmod 644 /home/user/firewall/iptables.rules && \
    rm -rf /home/user/audit

LABEL Author="OpenAI Assistant" \
      Description="Environment for SSH firewall audit task with pytest installed"