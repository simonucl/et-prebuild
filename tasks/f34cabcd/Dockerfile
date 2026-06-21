FROM ubuntu:22.04

# Author: ExampleCourse
# Description: Container for the “performance benchmark logging” exercise
# Version: 1.0

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping \
        procps && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONIOENCODING=utf-8
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"

# Ensure correct permissions at runtime
RUN chmod 755 /home/user

# Run-equivalent of the %runscript section (informational only)
CMD echo "Container for the performance benchmark logging exercise." && \
    echo "Open a shell inside the container to complete the assignment." && \
    /bin/bash