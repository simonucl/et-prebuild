FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create initial project layout
RUN mkdir -p /home/user/my_project/src && \
    mkdir -p /home/user/my_project/test && \
    mkdir -p /home/user/my_project/notes/tmp && \
    touch /home/user/my_project/src/old.tmp && \
    touch /home/user/my_project/src/main.c && \
    touch /home/user/my_project/test/data.tmp && \
    touch /home/user/my_project/debug.log && \
    touch /home/user/my_project/notes/tmp/info.tmp

# Permissions
RUN chmod -R 0777 /home/user

# Environment settings
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin"