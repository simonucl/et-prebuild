FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user

RUN FIREWALL_DIR="/home/user/firewall" && \
    mkdir -p "${FIREWALL_DIR}" && \
    chmod 755 "${FIREWALL_DIR}"

RUN cat > /home/user/firewall/active_rules.sh <<'EOF'
#!/bin/bash
# ACTIVE FIREWALL RULESET
# Managed by config-team
EOF

RUN chmod 644 /home/user/firewall/active_rules.sh

RUN : > /home/user/firewall/change_log.txt && \
    chmod 644 /home/user/firewall/change_log.txt

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8