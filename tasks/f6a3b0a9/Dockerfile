# Author="Your Name"
# Description="Container for API-checking assignment. Includes curl and pytest; /home/user exists but the assignment directory is intentionally absent."

FROM ubuntu:22.04

ENV PATH="$PATH:/usr/local/bin"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*