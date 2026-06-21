# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Base packages + pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create directory skeleton for the exercise
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/project/data_backup/20230115 && \
    mkdir -p /home/user/project/data_links && \
    mkdir -p /home/user/old_backups

# ------------------------------------------------------------------
# Populate validated backup files
# ------------------------------------------------------------------
RUN set -e && \
    printf 'Quarterly report – 2022 Q4\n'         > /home/user/project/data_backup/20230115/report.txt && \
    printf 'year,quarter,revenue\n2022,4,12345\n' > /home/user/project/data_backup/20230115/stats.csv && \
    printf 'PNGDATA\n'                            > /home/user/project/data_backup/20230115/image.png

# Ensure world-readable permissions (≥644 & ≤666)
RUN set -e && \
    chmod 664 /home/user/project/data_backup/20230115/report.txt && \
    chmod 664 /home/user/project/data_backup/20230115/stats.csv && \
    chmod 664 /home/user/project/data_backup/20230115/image.png

# ------------------------------------------------------------------
# Create the *broken* symlinks that the student must fix
# ------------------------------------------------------------------
RUN set -e && \
    ln -sf /home/user/old_backups/report.txt /home/user/project/data_links/report.txt && \
    ln -sf /home/user/old_backups/stats.csv  /home/user/project/data_links/stats.csv && \
    ln -sf /home/user/old_backups/image.png  /home/user/project/data_links/image.png

# ------------------------------------------------------------------
# Permissions: make sure the runtime (non-root) user can work
# ------------------------------------------------------------------
RUN set -e && \
    chmod -R a+rX,u+w,g+w,o+w /home/user && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment settings
# ------------------------------------------------------------------
ENV LANG=C.UTF-8

# ------------------------------------------------------------------
# Help
# Disaster-recovery drill container.
# Three validated backup files are placed under:
#     /home/user/project/data_backup/20230115/
# Broken symlinks under:
#     /home/user/project/data_links/
# The student must relink them and create the required log file.
# Pytest is installed for automated grading.
# ------------------------------------------------------------------