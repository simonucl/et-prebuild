FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial project structure expected by the tests
RUN set -e && \
    PROJECT_ROOT="/home/user/projects/backup-tool" && \
    BACKUPS_DIR="${PROJECT_ROOT}/backups" && \
    mkdir -p "${BACKUPS_DIR}" && \
    printf '1.2.3\n' > "${PROJECT_ROOT}/version.txt"

RUN cat > /home/user/projects/backup-tool/CHANGELOG.md <<'EOF'
## [1.2.3] - 2023-08-15
- Added incremental backup feature.

## [1.2.2] - 2023-07-01
- Initial release.
EOF

RUN printf 'BACKUP DATA 2023-01-01\n' > /home/user/projects/backup-tool/backups/backup_2023-01-01.txt && \
    printf 'BACKUP DATA 2023-02-01\n' > /home/user/projects/backup-tool/backups/backup_2023-02-01.txt && \
    printf 'BACKUP DATA 2023-03-03\n' > /home/user/projects/backup-tool/backups/backup_2023-03-01.txt && \
    chmod -R a+rwX /home/user

RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1