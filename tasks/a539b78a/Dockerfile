FROM ubuntu:22.04

# Container for the "daily backup verification" task.
# It provides:
#   • pytest (pre-installed)
#   • The expected initial directory tree and files under /home/user
#   • A writable /home/user so the student script can create verification.log

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/backups/daily && \
    mkdir -p /home/user/baselines

RUN : > /home/user/backups/daily/db.dump && \
    : > /home/user/backups/daily/config.tar.gz

RUN cat <<'EOF' > /home/user/baselines/daily.sha256
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  db.dump
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  config.tar.gz
EOF

RUN chmod a+rwX /home/user && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"