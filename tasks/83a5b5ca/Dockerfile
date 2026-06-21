FROM ubuntu:22.04

# Author="auto-generated"
# Description="Apptainer image for backup audit exercise (initial state)"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user || true && \
    mkdir -p /home/user/backups && \
    chmod 0777 /home/user/backups && \
    : > /home/user/backups/db.sql && \
    : > /home/user/backups/photos.tar.gz

RUN cat > /home/user/backups/sha256sums.txt <<'EOF'
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  db.sql
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa  photos.tar.gz
EOF

RUN chmod 0666 /home/user/backups/sha256sums.txt && \
    chown -R user:user /home/user && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin