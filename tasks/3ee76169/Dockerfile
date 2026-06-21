FROM ubuntu:22.04

# Help:
# This container includes pytest and an empty /home/user/firewall_config
# directory. Learners will create firewall configuration artefacts there.

# Label information
LABEL Author="firewall-config-demo"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/firewall_config && \
    chmod 777 /home /home/user /home/user/firewall_config && \
    rm -f /home/user/firewall_config/iptables.rules || true && \
    rm -f /home/user/firewall_config/changes.log || true

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user