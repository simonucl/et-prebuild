FROM ubuntu:22.04

# Help text from %runscript
# Container for the dummy restore task. Launch an interactive shell with:
# 'docker run -it --user user <image> /bin/bash' or run your commands directly.

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        procps \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user && \
    mkdir -p /home/user && \
    chown 1000:1000 /home/user && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*