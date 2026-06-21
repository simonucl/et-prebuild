FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create user and home directory
RUN useradd -m -d /home/user user && \
    chmod 755 /home/user

# Pre-populate backup data
RUN set -e && \
    BACKUP_ROOT="/home/user/backups/2023-10-03" && \
    mkdir -p "${BACKUP_ROOT}" && \
    printf 'SAMPLE DATABASE BACKUP 2023-10-03\n' > "${BACKUP_ROOT}/db_dump.sql.gz" && \
    printf 'PHOTOS ARCHIVE PLACEHOLDER\n' > "${BACKUP_ROOT}/photos.tar" && \
    printf 'CONFIG ZIP PLACEHOLDER\n'  > "${BACKUP_ROOT}/config.zip" && \
    chmod -R a+rX "${BACKUP_ROOT}" && \
    chmod -R a-w "${BACKUP_ROOT}"

# Directory for future reports
RUN REPORT_DIR="/home/user/backup_reports" && \
    mkdir -p "${REPORT_DIR}" && \
    chmod 0777 "${REPORT_DIR}"

# Environment
ENV HOME=/home/user

# Labels
LABEL Author="Container preparation for backup inventory task"
LABEL Description="Provides initial state (backup files) and pytest for automated grading."