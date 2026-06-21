FROM ubuntu:22.04

# Author "Auto-generated definition file for checksum verification task"

ENV PATH="/usr/local/bin:$PATH"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/it_assets

RUN chmod 755 /home && \
    chmod 755 /home/user && \
    chmod 755 /home/user/it_assets

RUN printf 'abc' > /home/user/it_assets/installer_v3.2.bin

RUN chmod 644 /home/user/it_assets/installer_v3.2.bin