FROM ubuntu:22.04

# Author "GPT-4"
# Description "Container for a disk-usage workflow exercise with pytest pre-installed and fixture data prepared."
# Help:
# This Apptainer image contains the initial filesystem state for the
# “disk-usage analysis” workflow. It provides:
# • Python 3 and pytest for automated grading
# • /home/user/disk_demo with two files totalling 25,600 bytes

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 1777 /home/user

RUN mkdir -p /home/user/disk_demo

RUN yes A | head -c 5120 > /home/user/disk_demo/file1.txt

RUN dd if=/dev/urandom bs=1024 count=20 of=/home/user/disk_demo/file2.bin conv=notrunc status=none

RUN chmod 755 /home/user/disk_demo && \
    chmod 644 /home/user/disk_demo/file1.txt /home/user/disk_demo/file2.bin