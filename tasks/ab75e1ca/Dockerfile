# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author example
# Description "Environment for image-modification log filtering exercise."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/workspace/reports

RUN cat <<'EOF' > /home/user/workspace/reports/change_history.log
[2023-11-01 09:12:45] ADD src/components/Header.js
[2023-11-01 09:12:46] MODIFY assets/logo.png
[2023-11-01 09:12:47] DELETE src/utils/helpers.py
[2023-11-01 09:12:48] MODIFY assets/banner.jpg
[2023-11-01 09:12:49] ADD README.md
[2023-11-01 09:12:50] MODIFY assets/icons/menu.svg
[2023-11-01 09:12:51] DELETE docs/old_manual.pdf
EOF

RUN chmod 755 /home/user/workspace/reports && \
    chmod 644 /home/user/workspace/reports/change_history.log