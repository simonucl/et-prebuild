FROM ubuntu:22.04

# Help / labels
LABEL Author="backup-task-preparer"
LABEL Description="Container for backup creation task – provides initial filesystem state and pytest."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/data && \
    echo "alpha" > /home/user/data/file1.txt && \
    echo "beta"  > /home/user/data/file2.txt

RUN mkdir -p /home/user/backup && \
    chmod 0777 /home/user/backup

RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1