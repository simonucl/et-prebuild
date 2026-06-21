FROM ubuntu:22.04

# Author edge-ai
# Description Base image for IoT-deployment exercise. Provides Python 3 and pytest,
# plus a clean /home/user directory. No workspace files are present.

RUN set -e && \
    echo "Updating package index and installing Python 3 + pip..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    echo "Installing pytest for the autograder..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating /home/user directory..." && \
    groupadd -g 1000 user 2>/dev/null || true && \
    useradd -m -d /home/user -u 1000 -g 1000 user 2>/dev/null || true && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="/home/user/.local/bin:${PATH}"

CMD ["/bin/bash"]