FROM ubuntu:22.04

# Help section not provided; none added.

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/audit_workspace

RUN cat > /home/user/audit_workspace/permissions_dump.txt <<'EOF'
-rw-r--r-- 1 alice auditors 1337 Jun 10 10:24 config.yml
-rwxr-xr-x 1 bob auditors 4096 Jun  5 09:12 run.sh
-rw-rw-r-- 1 carol auditors 2048 May 30 14:00 notes.txt
-rw-r--r-- 1 dave auditors 5120 Apr 21 08:45 backup.tar
-rwxrwxrwx 1 eve auditors   64 Jun 11 11:11 dangerous.sh
EOF

RUN chmod -R 0777 /home/user/audit_workspace

RUN chmod 755 /home/user