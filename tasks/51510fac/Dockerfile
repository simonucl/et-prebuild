FROM ubuntu:22.04

# From %post
RUN set -e && \
    echo "Updating package index and installing system packages..." && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iproute2 \
        net-tools \
        procps \
        util-linux && \
    echo "Installing pytest for the test harness..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating writable home directory for the student user..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    echo "Cleaning up apt caches to keep the image small..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# From %environment
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin

# Additional environment commands requiring shell operations
RUN chmod 755 /home/user

# From %labels
LABEL Author="Container Build Script"
LABEL Description="Base image for the Build Diagnostics Report assignment with pytest pre-installed."

# From %help
# This container provides a clean Ubuntu 22.04 environment with pytest installed.
# No assignment artifacts are pre-created; students must generate them during their task execution.