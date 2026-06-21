FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare a writable baseline home directory for the student
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Replicate runscript behavior: chmod home on container start, then exec passed command
ENTRYPOINT ["/bin/bash", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]