FROM ubuntu:22.04

# Help text
# This container provides a minimal Ubuntu 22.04 environment with
# Python, pytest, make, and standard compression utilities installed.
# A non-root user "user" (UID/GID 1000) with home directory /home/user
# is pre-created to allow the grading agent to operate without
# elevated privileges.

# Author and description labels
LABEL Author="backup_demo_container"
LABEL Description="Base image for the backup demo task with pytest installed."

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        make \
        tar \
        gzip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user || true && \
    mkdir -p /home/user && \
    chown -R 1000:1000 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH=/home/user/.local/bin:$PATH

USER user

CMD ["/bin/bash"]