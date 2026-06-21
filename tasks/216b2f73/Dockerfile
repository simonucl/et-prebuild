FROM ubuntu:22.04

# Help:
# This container provides a minimal Ubuntu 22.04 environment with Python 3
# and pytest installed. The /home/user directory is writable so that
# students can complete the “serverwatch” alert-rules creation task.

RUN set -eux && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

CMD ["/bin/bash"]