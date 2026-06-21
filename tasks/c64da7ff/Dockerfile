# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help section from Apptainer
# Default action: start a shell

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/backup_logs && \
    chmod 0777 /home/user

RUN cat >/home/user/backup_logs/2023-10-21.log <<'EOF'
2023-10-21 02:00:01 STATUS=OK     SIZE=155662721 SHA256=1ab4c9fed9c0ad53a7e3d0d39af0b3e2ab0e7fb9176c91b8b9daf4d5e67cd1a7
2023-10-21 02:00:02 STATUS=FAILED SIZE=0         SHA256=0000000000000000000000000000000000000000000000000000000000000000
2023-10-21 02:00:03 STATUS=OK     SIZE=178662733 SHA256=2bb4c9fed9c0ad53a7e3d0d39af0b3e2ab0e7fb9176c91b8b9daf4d5e67cd1b8
EOF

RUN cat >/home/user/backup_logs/2023-10-22.log <<'EOF'
2023-10-22 02:00:01 STATUS=OK     SIZE=156772821 SHA256=3cb4c9fed9c0ad53a7e3d0d39af0b3e2ab0e7fb9176c91b8b9daf4d5e67cd1c9
2023-10-22 02:00:02 STATUS=FAILED SIZE=0         SHA256=0000000000000000000000000000000000000000000000000000000000000000
2023-10-22 02:00:03 STATUS=FAILED SIZE=0         SHA256=0000000000000000000000000000000000000000000000000000000000000000
EOF

RUN cat >/home/user/backup_logs/2023-10-23.log <<'EOF'
2023-10-23 02:00:01 STATUS=OK     SIZE=167882921 SHA256=4db4c9fed9c0ad53a7e3d0d39af0b3e2ab0e7fb9176c91b8b9daf4d5e67cd1da
2023-10-23 02:00:02 STATUS=OK     SIZE=168992931 SHA256=5eb4c9fed9c0ad53a7e3d0d39af0b3e2ab0e7fb9176c91b8b9daf4d5e67cd1eb
2023-10-23 02:00:03 STATUS=FAILED SIZE=0         SHA256=0000000000000000000000000000000000000000000000000000000000000000
EOF

RUN chmod 644 /home/user/backup_logs/*.log && \
    chmod 755 /home/user

CMD ["/bin/bash"]