FROM ubuntu:22.04

# Help:
# This container provides the initial cleaned dataset and a Python/pytest
# environment so that students can work on the backup & manifest task
# described in the assignment.

LABEL Author="YourName"
LABEL Description="Environment for image-classification dataset backup task"

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN install -d -m 0755 /home/user/datasets/images && \
    install -d -m 0755 /home/user/datasets/labels

RUN printf "fake image data 1\n" > /home/user/datasets/images/img1.jpg && \
    printf "fake image data 2\n" > /home/user/datasets/images/img2.jpg && \
    printf "label for image 1\n" > /home/user/datasets/labels/img1.txt && \
    printf "label for image 2\n" > /home/user/datasets/labels/img2.txt

RUN chmod 0644 /home/user/datasets/images/img1.jpg && \
    chmod 0644 /home/user/datasets/images/img2.jpg && \
    chmod 0644 /home/user/datasets/labels/img1.txt && \
    chmod 0644 /home/user/datasets/labels/img2.txt

RUN install -d -m 0755 /home/user/backups

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH