FROM ubuntu:22.04

# Converted from Apptainer definition file (Bootstrap: localimage ./ubuntu_22.04.sif)

RUN set -e && \
    echo "Updating package index and installing required packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools

RUN echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating initial directory structure and input file..." && \
    mkdir -p /home/user/env_setup && \
    chmod 755 /home /home/user /home/user/env_setup

RUN cat << 'EOF' > /home/user/env_setup/targets.txt
dev
qa
staging
qa
dev
prod
qa
EOF

RUN chmod 644 /home/user/env_setup/targets.txt

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Original runscript (not directly applicable in Docker):
# chmod 755 /home/user
# echo "Container for QA environment frequency task. Use bash to explore."
# exec /bin/bash "$@"