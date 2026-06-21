# This container provides a minimal Ubuntu 22.04 environment with Python 3 and
# pytest installed, plus a writable /home/user directory expected by the
# automated tests for the “UTC time-zone & en_US.UTF-8 locale compliance” task.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    locale-gen en_US.UTF-8 && \
    update-locale && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin

CMD ["/bin/bash"]