# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Installing Python tooling..." && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Creating initial backup directory structure..." && \
    mkdir -p /home/user/backup/2023-09-15 && \
    chmod 0755 /home/user && \
    chmod 0777 /home/user/backup && \
    chmod 0755 /home/user/backup/2023-09-15 && \
    printf 'a'   > /home/user/backup/2023-09-15/original1.txt && \
    printf 'abc' > /home/user/backup/2023-09-15/original2.txt && \
    :            > /home/user/backup/2023-09-15/original3.txt

RUN cat > /home/user/backup/2023-09-15/checksums.sha256 <<'EOF'
ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb  original1.txt
ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad  original2.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  original3.txt
EOF

RUN chmod 0644 /home/user/backup/2023-09-15/original1.txt && \
    chmod 0644 /home/user/backup/2023-09-15/original2.txt && \
    chmod 0644 /home/user/backup/2023-09-15/original3.txt && \
    chmod 0644 /home/user/backup/2023-09-15/checksums.sha256 && \
    echo "Setup complete."

RUN chmod 755 /home/user

ENV PYTHONIOENCODING=utf-8

LABEL Author="backup-integrity-scenario"