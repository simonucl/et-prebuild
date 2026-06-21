# Author performance-engineering-setup
# Description Base image for “profiling environment variables” exercise
FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user

ENV PATH="/usr/local/bin:$PATH"

# Default runscript behavior
CMD ["bash"]