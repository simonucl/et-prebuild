FROM ubuntu:22.04

# Help text
# This container provides the starting environment for the symlink-fixing
# exercise. All initial directories, files, and (intentionally incorrect)
# symbolic links are pre-created under /home/user. The student’s task is
# to correct those links and update the associated log once the container
# is running.

LABEL Author="OpenAI ChatGPT"
LABEL Description="Container for the symlink correction exercise"

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/network_configs/siteA_v1 && \
    mkdir -p /home/user/network_configs/siteA_v2 && \
    mkdir -p /home/user/bin && \
    mkdir -p /home/user/tools

RUN ln -s siteA_v1 /home/user/network_configs/active

RUN : > /home/user/network_configs/symlink_changes.log

RUN ln -s ../scripts/ping-test.sh /home/user/bin/ping-test && \
    ln -s ../scripts/ip-test.sh /home/user/bin/ip-test

RUN cat >/home/user/tools/ip-test.sh <<'EOF'
#!/bin/bash
echo 'ip test'
EOF

RUN chmod +x /home/user/tools/ip-test.sh

RUN chmod -R a+rwX /home/user