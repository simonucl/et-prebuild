FROM ubuntu:22.04

# Help section
# This container is set up for the ML data-prep task. Use 'apptainer exec' to run commands.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        zip \
        unzip \
        xz-utils \
        tar \
        coreutils && \
    ln -s /usr/bin/python3 /usr/local/bin/python || true && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/source_images && \
    mkdir -p /home/user/source_labels && \
    yes "A" | head -c 81  > /home/user/source_images/cat.jpg && \
    yes "B" | head -c 82  > /home/user/source_images/dog.jpg && \
    yes "C" | head -c 83  > /home/user/source_images/bird.jpg && \
    echo '{"label":"cat"}'  > /home/user/source_labels/cat.json && \
    echo '{"label":"dog"}'  > /home/user/source_labels/dog.json && \
    echo '{"label":"bird"}' > /home/user/source_labels/bird.json && \
    chmod 0644 /home/user/source_images/*.jpg && \
    chmod 0644 /home/user/source_labels/*.json && \
    chmod 0755 /home/user/source_images /home/user/source_labels && \
    chmod 755 /home/user

ENV HOME=/home/user