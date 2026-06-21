FROM ubuntu:22.04

# Labels
LABEL Author="firewall-hardening-task"
LABEL Description="Base image with Python and pytest installed; prepared for firewall hardening exercise."

# Post installation
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates \
        bash && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    chown -R user:user /home/user && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Default entrypoint
ENTRYPOINT ["/bin/bash", "-c", "exec \"$@\"", "--"]