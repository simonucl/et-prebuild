FROM ubuntu:22.04

# %post
RUN set -e && \
    echo "Updating apt package index..." && \
    apt-get update -qq && \
    echo "Installing required system packages..." && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        openssl \
        coreutils \
        tar \
        gzip \
        python3 \
        python3-pip && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating writable /home/user directory..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    echo "Cleaning up apt caches..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# %environment
RUN chmod 755 /home/user
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin