FROM ubuntu:22.04

# Help section not provided

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        curl \
        ca-certificates \
        --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

RUN useradd -m -s /bin/bash user && \
    mkdir -p /home/user/project && \
    printf 'Project README\n' > /home/user/project/README.md && \
    chown -R user:user /home/user

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"