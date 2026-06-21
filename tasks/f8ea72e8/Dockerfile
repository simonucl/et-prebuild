FROM ubuntu:22.04

# Author: ExampleDeveloper
# Description: "Environment for the gzip-compression reporting task"
# Help:
# This container provides the initial state required for the
# “compression report” assignment. The original JavaScript and CSS
# files are present, while the compressed files and report log are
# purposefully absent. Pytest is installed for automated grading.

ENV PATH="/usr/local/bin:${PATH}"

RUN chmod 755 /home || true

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gzip \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

RUN ASSETS_DIR=/home/user/webapp/assets && \
    mkdir -p "${ASSETS_DIR}" && \
    for i in $(seq 1 100); do printf "console.log('hello performance');\n"; done > "${ASSETS_DIR}/main.js" && \
    for i in $(seq 1 100); do printf "body { margin: 0; padding: 0; }\n"; done > "${ASSETS_DIR}/style.css" && \
    chown -R 1000:1000 /home/user && \
    chmod 0644 "${ASSETS_DIR}/main.js" "${ASSETS_DIR}/style.css"