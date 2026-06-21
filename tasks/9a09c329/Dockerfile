FROM ubuntu:22.04

# Help / description
# Author task-prep-bot
# Description: Container for SQLite local database task – includes sqlite3 and pytest.

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/projects && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user