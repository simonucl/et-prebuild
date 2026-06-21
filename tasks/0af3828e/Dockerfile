# Converted from Apptainer definition file
FROM ubuntu:22.04

# Update apt and install Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem state
RUN mkdir -p /home/user/images && \
    mkdir -p /home/user/archive && \
    touch /home/user/images/ubuntu_latest.sif && \
    touch /home/user/images/debian_tools.sif && \
    touch /home/user/images/archdev.sif && \
    touch /home/user/archive/old_centos.sif && \
    chmod 1777 /home/user && \
    chmod 0777 /home/user/images && \
    chmod 0777 /home/user/archive

# From %environment section
RUN chmod 755 /home/user
ENV PYTHONIOENCODING=UTF-8