FROM ubuntu:22.04

# Author NetDiag-Container-Builder
# Description: Base container for the 'netdiag' task. Provides Python, pytest, and needed networking utilities.

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

RUN set -e && \
    echo "Updating package lists..." && \
    apt-get update && \
    echo "Installing required packages..." && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping \
        procps \
        locales && \
    echo "Generating locale..." && \
    locale-gen en_US.UTF-8 && \
    echo "Installing pytest..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating home directory..." && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    echo "Cleaning APT caches..." && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

CMD /bin/sh -c "echo 'This container is prepared for the netdiag task.' && echo 'Open a shell inside the container to begin working.'"