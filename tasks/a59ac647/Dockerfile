FROM ubuntu:22.04

# Author: release-manager-setup
# Version: 1.0

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/old_code

RUN cat <<'EOF' >/home/user/old_code/release.sh
#!/bin/sh
# Legacy release script
if [ "$1" = "--version" ]; then
    echo "old_code release v0.9.8"
    exit 0
fi

echo "Usage: $0 --version"
exit 1
EOF

RUN chmod 755 /home/user/old_code/release.sh

ENV LC_ALL=C.UTF-8
ENV PATH=/home/user/old_code:$PATH