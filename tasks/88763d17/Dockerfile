FROM ubuntu:22.04

# Update package index and install required utilities
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        net-tools \
        iputils-ping \
        dnsutils && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    rm -rf /var/lib/apt/lists/*

# Commands from %environment that are not variable exports
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Run script
CMD /bin/sh -c "echo 'Container for networking-snapshot provisioning task.' && echo 'Invoke your own scripts or commands inside this container as needed.'"