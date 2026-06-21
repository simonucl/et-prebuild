# Converted from Apptainer definition file
FROM ubuntu:22.04

# Help text
# This container provides the initial environment for the “backup automation”
# Makefile assignment. Pytest is installed, and the seed data set is located
# in /home/user/project/data/file1.txt.

# Labels
LABEL Author="backup-automation-task"

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        tar \
        gzip \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/data && \
    printf 'Sample data for backup.\n' > /home/user/project/data/file1.txt && \
    chmod -R 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Apply chmod required by %environment that is not an ENV var
RUN chmod 755 /home/user