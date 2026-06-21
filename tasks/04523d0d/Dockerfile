FROM ubuntu:22.04

# Labels
LABEL Author="backup-task-container-setup"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip \
        ca-certificates \
        coreutils && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN adduser --disabled-password --gecos "" user

RUN mkdir -p /home/user/data/projects && \
    mkdir -p /home/user/data/reports && \
    mkdir -p /home/user/archives && \
    mkdir -p /home/user/backup_logs

RUN printf "Project README\n"               > /home/user/data/projects/readme.txt && \
    printf 'print("Hello World")\n'         > /home/user/data/projects/code.py && \
    printf "Quarterly report Q1\n"          > /home/user/data/reports/report1.txt

RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod -R 755 /home/user/data && \
    chmod 644 /home/user/data/projects/readme.txt && \
    chmod 644 /home/user/data/projects/code.py && \
    chmod 644 /home/user/data/reports/report1.txt && \
    chmod 777 /home/user/archives && \
    chmod 777 /home/user/backup_logs

CMD echo "Container for backup-task ready. Launch your commands."