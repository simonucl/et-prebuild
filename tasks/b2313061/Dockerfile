# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        cron \
        python3-pip

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/backup

RUN cat <<'EOF' >/home/user/backup/cleanup.sh
#!/bin/bash
# Dummy maintenance script – learners will reference this in their cron job.
echo "Running cleanup tasks..."
EOF

RUN chmod +x /home/user/backup/cleanup.sh

RUN chmod 755 /home/user && chmod 755 /home/user/backup

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*

# Help and runscript from Apptainer omitted because Docker does not use runscript.