# Based on Apptainer Bootstrap: localimage (converted to Docker base image)
FROM ubuntu:22.04

# Help text from %help
# This image provides the starting environment for the
# "file-extension frequency summary" exercise.
# • Working directory: /home/user/disk_usage
# • Source file:       raw_file_list.txt (17 lines)
# • Task:              Generate extension_frequency.log
# Pytest is pre-installed for automated checking.

LABEL Author="Your Name"
LABEL Description="Environment for disk-usage extension frequency task – includes pytest and pre-populated data."

ENV PATH=/usr/local/bin:/usr/bin:/bin

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata \
        locales && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/disk_usage && \
    chmod 755 /home/user && \
    chmod 755 /home/user/disk_usage

RUN cat >/home/user/disk_usage/raw_file_list.txt <<'EOF'
.log
.tmp
.log
.bak
.log
.txt
.tmp
.csv
.csv
.txt
.log
.bak
.iso
.iso
.tmp
.log
.img
EOF

RUN chmod 644 /home/user/disk_usage/raw_file_list.txt

RUN apt-get clean && rm -rf /var/lib/apt/lists/*