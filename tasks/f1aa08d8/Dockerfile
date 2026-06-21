# Converted from Apptainer definition file
FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory hierarchy and snapshot files
RUN mkdir -p /home/user && \
    chmod 777 /home/user && \
    mkdir -p /home/user/backup_source/docs && \
    mkdir -p /home/user/backup_source/images && \
    printf "hello world" > /home/user/backup_source/docs/report.txt && \
    printf "abc" > /home/user/backup_source/images/logo.txt && \
    chmod 755 /home/user/backup_source && \
    chmod 755 /home/user/backup_source/docs && \
    chmod 755 /home/user/backup_source/images && \
    chmod 644 /home/user/backup_source/docs/report.txt && \
    chmod 644 /home/user/backup_source/images/logo.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8