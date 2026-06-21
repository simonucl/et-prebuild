FROM ubuntu:22.04

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Prepare initial on-disk layout for the assignment
# 1. Base directory for the user
RUN mkdir -p /home/user && \
    chmod 1777 /home/user

# 2. Project tree
RUN mkdir -p /home/user/project/logs && \
    mkdir -p /home/user/project/scripts && \
    mkdir -p /home/user/project/tmp

# Directory permissions
RUN chmod 0755 /home/user/project && \
    chmod 0777 /home/user/project/logs && \
    chmod 0755 /home/user/project/scripts && \
    chmod 1777 /home/user/project/tmp

# 3. Regular files with exact permission bits
RUN echo 'dummy db'                > /home/user/project/data.db && \
    echo '#!/bin/bash'             > /home/user/project/file1.sh && \
    echo 'placeholder'             > /home/user/project/file2.txt && \
    echo 'log entry'               > /home/user/project/logs/app.log && \
    printf '#!/bin/bash\necho Installing\n' > /home/user/project/scripts/install.sh && \
    echo 'cache'                   > /home/user/project/tmp/cache.tmp

RUN chmod 0666 /home/user/project/data.db && \
    chmod 0644 /home/user/project/file1.sh && \
    chmod 0664 /home/user/project/file2.txt && \
    chmod 0644 /home/user/project/logs/app.log && \
    chmod 0755 /home/user/project/scripts/install.sh && \
    chmod 0666 /home/user/project/tmp/cache.tmp

# Set up entrypoint to handle permissions and execute commands
RUN echo '#!/bin/bash\nchmod 755 /home/user\nexec "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]