FROM ubuntu:22.04

# Author integration-task-generator
# Description Base image for "API availability check" exercise

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 0777 /home/user

ENV PYTHONIOENCODING=utf-8
ENV PATH="/usr/local/bin:${PATH}"

# Ensure default permissions at container start
RUN chmod 755 /home/user

# Equivalent of runscript
CMD echo "Container for the API availability check exercise." && \
    echo "Enter the container with 'docker run -it' or 'docker exec -it' to start working."