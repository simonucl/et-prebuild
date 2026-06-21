FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/datasets/images && \
    mkdir -p /home/user/datasets/texts && \
    mkdir -p /home/user/datasets/videos

RUN dd if=/dev/zero of=/home/user/datasets/images/img.bin bs=1000 count=2048 status=none

RUN dd if=/dev/zero of=/home/user/datasets/texts/story.txt bs=1024 count=1024 status=none

RUN dd if=/dev/zero of=/home/user/datasets/videos/clip.mkv bs=1024 count=5120 status=none

RUN chmod -R a+rX /home/user/datasets

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# This container sets up the environment for the disk-usage reporting task.