FROM ubuntu:22.04

# Install Python + pip, then pytest
RUN set -e && \
    DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a dedicated non-privileged account that will own /home/user
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user; \
    fi

# Prepare the on-disk tree required by the tests
RUN WS="/home/user/workspace" && \
    mkdir -p "${WS}/temp" && \
    printf 'TOP SECRET\n' > "${WS}/confidential.txt" && \
    printf 'public info\n' > "${WS}/public.log" && \
    printf '#!/bin/sh\n' > "${WS}/script.sh" && \
    touch "${WS}/temp/temp.db" && \
    printf '#!/bin/sh\n' > "${WS}/temp/world.sh"

# Set the precise permission bits for every path
RUN WS="/home/user/workspace" && \
    chmod 0755 /home/user && \
    chmod 0755 "${WS}" && \
    chmod 0600 "${WS}/confidential.txt" && \
    chmod 0666 "${WS}/public.log" && \
    chmod 0755 "${WS}/script.sh" && \
    chmod 0755 "${WS}/temp" && \
    chmod 0664 "${WS}/temp/temp.db" && \
    chmod 0777 "${WS}/temp/world.sh" && \
    chown -R user:user /home/user

# Labels
LABEL Author="Automation Workflow Specialist"