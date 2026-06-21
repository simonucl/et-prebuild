FROM ubuntu:22.04

# Help/comment section
# Author incident-prep
# Description: Base image for incident-response exercise; pytest installed, initial filesystem state prepared.

RUN set -e; \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iputils-ping && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    rm -rf /var/lib/apt/lists/*

# Environment setup from %environment
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

LABEL Author="incident-prep"
LABEL Description="Base image for incident-response exercise; pytest installed, initial filesystem state prepared."

CMD echo "Container for incident-response exercise. Launch an interactive shell to begin."