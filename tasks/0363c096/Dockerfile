FROM ubuntu:22.04

# Author: Pip-Package-Inventory
# Description: Base image for the “pip package inventory” task. Provides Python, pip, pytest, and ensures /home/user exists while leaving the etl workspace empty.

LABEL Author="Pip-Package-Inventory" \
      Description="Base image for the pip package inventory task."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

CMD ["bash"]