FROM ubuntu:22.04

# Help / runscript notes
# This container is prepared for the backup-and-restore exercise.
# Start an interactive shell with: apptainer exec <image> /bin/bash

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        locales \
        tzdata \
        python3 \
        python3-pip \
        tar && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    echo "fr_FR.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

CMD /bin/bash -c "echo 'This container is prepared for the backup-and-restore exercise.' && echo 'Start an interactive shell with: docker run -it <image> /bin/bash'"