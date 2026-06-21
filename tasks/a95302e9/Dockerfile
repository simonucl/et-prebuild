# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# This Apptainer image sets up the initial filesystem state for the
# symlink-management task and includes pytest for automated evaluation.

LABEL Author="Automation"
LABEL Description="Container for symlink exercise with initial state prepared and pytest installed."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/dev/bin && \
    mkdir -p /home/user/bin

RUN cat <<'EOF' > /home/user/dev/bin/run_backup.sh
#!/usr/bin/env bash
echo "Running backup..."
EOF

RUN cat <<'EOF' > /home/user/dev/bin/check_status.sh
#!/usr/bin/env bash
echo "Checking status..."
EOF

RUN chmod +x /home/user/dev/bin/run_backup.sh /home/user/dev/bin/check_status.sh

RUN ln -sfn /usr/local/bin/run_backup_old /home/user/bin/run_backup

RUN chmod -R 777 /home/user

RUN chmod 755 /home/user