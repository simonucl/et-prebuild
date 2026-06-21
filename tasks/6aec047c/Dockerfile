# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer Task Prep" \
      Description="Base image for loop-back connectivity automation task with pytest installed"

# Post section: install packages, create user, clean up
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        make \
        iputils-ping \
        traceroute && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for grading
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create a non-privileged user `user` with home directory /home/user
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g user -s /bin/bash user && \
    chown -R user:user /home/user

# Ensure correct permissions and remove any remnants of the exercise directory
RUN chmod 755 /home/user && \
    rm -rf /home/user/netdiag || true

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Default action: start an interactive shell
CMD ["/bin/bash"]