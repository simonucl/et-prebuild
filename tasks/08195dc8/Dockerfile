FROM ubuntu:22.04

# Help / metadata from %labels
LABEL Author="Infrastructure Exercise Setup"
LABEL Description="Minimal environment for the Infrastructure Provisioning task"

# Basic tooling
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial exercise state
RUN mkdir -p /home/user/provisioning/config && \
    mkdir -p /home/user/provisioning/scripts && \
    mkdir -p /home/user/provisioning/docs

RUN printf 'port=8080\nmode=production\n' > /home/user/provisioning/config/app.conf

RUN printf '#!/bin/bash\necho Deploying...\n' > /home/user/provisioning/scripts/deploy.sh && \
    chmod +x /home/user/provisioning/scripts/deploy.sh

RUN printf '# Infrastructure Provisioning\nThis directory contains scripts.\n' > /home/user/provisioning/docs/readme.md

RUN chmod 644 /home/user/provisioning/config/app.conf \
              /home/user/provisioning/scripts/deploy.sh \
              /home/user/provisioning/docs/readme.md

# chmod from labels section
RUN chmod 755 /home/user

# Run section
CMD echo "This container is prepared for the Infrastructure Provisioning exercise." && \
    echo "Invoke your own commands or a test suite as needed."