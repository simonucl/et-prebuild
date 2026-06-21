FROM ubuntu:22.04

# Labels
LABEL Author="task-preparer"
LABEL Description="Base image for network audit task – installs pytest and ensures writable /home/user."

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Update package list and install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iproute2 \
        iputils-ping && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user

CMD ["echo", "Container for network audit task is ready."]