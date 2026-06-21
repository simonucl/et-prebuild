FROM ubuntu:22.04

# Update package lists and install required software.
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply environment-time permissions setup
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8