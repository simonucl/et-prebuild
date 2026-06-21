FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user

RUN cat << 'EOF' > /home/user/current_firewall.txt
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -p tcp -m tcp --dport 80  -j ACCEPT
-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 22  -j ACCEPT
-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
-A INPUT -p tcp -m tcp --dport 8080 -j DROP
-A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
EOF

# Permissions:
#   - Directory needs to be writable by the runtime user so they can create
#     /home/user/port443_count.log.
#   - The firewall file itself must be read-only.
RUN chmod 777 /home/user && \
    chmod 444 /home/user/current_firewall.txt

# Ensure standard paths are present
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH