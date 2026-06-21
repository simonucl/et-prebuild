FROM ubuntu:22.04

# Author="Apptainer setup for backup strategy task"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    groupadd -r user && \
    useradd -m -r -g user user && \
    mkdir -p /home/user/infrastructure/configs && \
    mkdir -p /home/user/infrastructure/scripts && \
    mkdir -p /home/user/infrastructure/tmp

RUN cat >/home/user/infrastructure/configs/app.conf <<'EOF'
port=8080
threads=4
mode=production
EOF

RUN cat >/home/user/infrastructure/configs/db.conf <<'EOF'
host=localhost
port=5432
user=infra
EOF

RUN cat >/home/user/infrastructure/scripts/deploy.sh <<'EOF'
#!/bin/bash
echo "Deploying..."
EOF

RUN chmod +x /home/user/infrastructure/scripts/deploy.sh

RUN echo "scratch" >/home/user/infrastructure/tmp/cache.tmp

RUN chmod -R a+rX /home/user/infrastructure && \
    chown -R user:user /home/user/infrastructure && \
    chown user:user /home/user && \
    rm -rf /home/user/backup_archives || true && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin