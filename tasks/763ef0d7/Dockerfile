# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package lists and install required packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip iptables && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Adjust permissions for the home directory
RUN chmod 755 /home/user

# Ensure user-installed Python tools are discoverable
ENV PATH="/home/user/.local/bin:${PATH}"

# Apptainer container for the firewall provisioning task.
CMD ["bash"]