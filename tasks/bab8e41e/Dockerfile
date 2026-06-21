# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv \
        ca-certificates \
        git \
        sudo && \
    pip3 install --no-cache-dir pytest && \
    groupadd --gid 1000 user && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash user && \
    if [ -f /etc/skel/.bashrc ]; then cp /etc/skel/.bashrc /home/user/.bashrc; else touch /home/user/.bashrc; fi && \
    chown -R user:user /home/user && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment section
RUN chmod 755 /home/user
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Labels section
LABEL Author="Apptainer Task Provisioner"
LABEL Description="Base image for Android CI bootstrap exercise"

# Runscript equivalent
# Default command: start a shell
CMD ["/bin/bash"]