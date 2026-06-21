# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="Apptainer build script for disk utilisation task" \
      Version="1.0"

ENV LC_ALL=C.UTF-8 \
    PYTHONIOENCODING=utf-8

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the exercise
RUN set -eux && \
    mkdir -p /home/user/disk_usage && \
    chmod 755 /home/user && \
    chmod 755 /home/user/disk_usage

RUN cat > /home/user/disk_usage/full_report.tsv <<'EOF'
Server	Mount	Total_GB	Used_GB	Free_GB	Use_percent
srv1	/	500	350	150	70%
srv2	/	1000	600	400	60%
srv3	/data	2000	1200	800	60%
srv4	/backup	1500	1200	300	80%
EOF

RUN chmod 644 /home/user/disk_usage/full_report.tsv