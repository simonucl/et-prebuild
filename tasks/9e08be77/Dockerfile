FROM ubuntu:22.04

# Help / metadata (from %help and %labels)
# Author: Auto-generated
# Description: Environment for audit-trail task: no world-writable executables under /home/user/public_data except the intentional one

# Base packages and Python tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash \
        coreutils \
        util-linux && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user “user” with UID/GID 1000
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# Directory tree and files
RUN install -d -o user -g user -m 755 /home/user/public_data/bin && \
    install -d -o user -g user -m 755 /home/user/public_data/scripts && \
    install -d -o user -g user -m 755 /home/user/audit && \
    touch /home/user/public_data/clean_readme.txt && \
    chown user:user /home/user/public_data/clean_readme.txt && \
    chmod 0644 /home/user/public_data/clean_readme.txt && \
    echo '#!/bin/bash' > /home/user/public_data/bin/tool && \
    chown user:user /home/user/public_data/bin/tool && \
    chmod 0755 /home/user/public_data/bin/tool && \
    echo '#!/bin/bash' > /home/user/public_data/scripts/run.sh && \
    chown user:user /home/user/public_data/scripts/run.sh && \
    chmod 0775 /home/user/public_data/scripts/run.sh && \
    echo '#!/bin/bash' > /home/user/public_data/scripts/unsafe.sh && \
    chown user:user /home/user/public_data/scripts/unsafe.sh && \
    chmod 0777 /home/user/public_data/scripts/unsafe.sh

# Environment setup
RUN chmod 755 /home/user
ENV PATH=/home/user/public_data/bin:$PATH

# Default runscript behavior
CMD ["/bin/bash"]