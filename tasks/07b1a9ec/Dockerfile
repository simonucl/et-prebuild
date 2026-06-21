FROM ubuntu:22.04

# Author YourName
# Description "Base image for FinOps profile exercise – Ubuntu 22.04 with pytest pre-installed."
# This container is prepared for the FinOps profile exercise.
# It contains:
#   • Ubuntu 22.04 base system
#   • Python 3 and pytest (for automated assessment)
# The /home/user directory is pre-created and writable.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales && \
    sed -Ei 's/^# (en_US.UTF-8 UTF-8)/\1/' /etc/locale.gen && \
    locale-gen && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="$PATH:/home/user/.local/bin"

CMD ["bash"]