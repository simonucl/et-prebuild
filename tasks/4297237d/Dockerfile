FROM ubuntu:22.04

# Author build-bot
# Description: Environment for SSH key-pair creation assignment (pytest pre-checks only).

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-client \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN if ! getent group 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user; \
    fi

RUN if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

RUN chmod 0755 /home/user

RUN echo 'export PATH="$HOME/.local/bin:$PATH"' >> /home/user/.bashrc

ENV PATH="/home/user/.local/bin:$PATH"