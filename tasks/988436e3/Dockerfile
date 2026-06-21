# Author: Storage-Reports Task Builder
# Version: v1.0

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        sqlite3 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin

# Original runscript:
# echo "Apptainer container ready for the disk-space monitoring task."
# echo "Launch your shell commands within this environment."
# exec /bin/bash "$@"

CMD ["/bin/bash"]