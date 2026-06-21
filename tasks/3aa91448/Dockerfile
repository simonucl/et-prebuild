FROM ubuntu:22.04

# Base packages + Python tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip iptables ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create non-privileged user
RUN useradd -m -s /bin/bash user || true

# Directory structure
RUN mkdir -p /home/user/firewall_rules && \
    mkdir -p /home/user/logs

# initial_rules.v4
RUN cat <<'EOF' > /home/user/firewall_rules/initial_rules.v4
*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
# Allow established
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
# Allow loopback
-A INPUT -i lo -j ACCEPT
# Wide-open rule that must stay last
-A INPUT -p tcp -j ACCEPT
COMMIT
EOF

# packet.log
RUN cat <<'EOF' > /home/user/logs/packet.log
2023-10-05T12:01:01Z SRC=203.0.113.45 DST=192.0.2.10 LEN=60 PROTO=TCP
2023-10-05T12:01:05Z SRC=198.51.100.23 DST=192.0.2.10 LEN=60 PROTO=TCP
2023-10-05T12:03:01Z SRC=203.0.113.45 DST=192.0.2.11 LEN=60 PROTO=TCP
2023-10-05T12:05:01Z SRC=198.51.100.47 DST=192.0.2.10 LEN=60 PROTO=TCP
2023-10-05T12:07:01Z SRC=203.0.113.45 DST=192.0.2.12 LEN=60 PROTO=TCP
2023-10-05T12:09:01Z SRC=198.51.100.23 DST=192.0.2.13 LEN=60 PROTO=TCP
EOF

# Permissions
RUN chown -R user:user /home/user && \
    chmod 0777 /home/user/firewall_rules && \
    chmod 0777 /home/user/logs && \
    chmod 0644 /home/user/firewall_rules/initial_rules.v4 && \
    chmod 0644 /home/user/logs/packet.log && \
    chmod 755 /home/user

# Environment
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD ["/bin/bash"]