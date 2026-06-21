# Author example
# Description: Container for ML data-prep task: provides initial raw_images and pytest.

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/raw_images

RUN set -eux && \
    for img in cat.jpg dog.jpg bird.jpg logo.png; do \
        echo "dummy data for $img" > "/home/user/raw_images/${img}"; \
    done

RUN chmod -R a+rX /home/user/raw_images && \
    chmod 755 /home/user