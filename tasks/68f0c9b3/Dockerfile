# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare the initial filesystem state
RUN mkdir -p /home/user/restores/2024-06-10

RUN cat <<'EOF' > /home/user/restores/2024-06-10/daily_filelist.log
docs/finance/report1.pdf
docs/hr/policy.docx
media/photos/img001.jpg
docs/finance/report1.pdf
media/photos/img002.jpg
docs/finance/report1.pdf
media/photos/img001.jpg
docs/hr/policy.docx
scripts/backup.sh
scripts/backup.sh
scripts/backup.sh
media/photos/img002.jpg
media/photos/img002.jpg
EOF

# Set liberal permissions so the non-root user inside the container can read/write
RUN chmod -R a+rwx /home/user

# Runtime environment setup
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1