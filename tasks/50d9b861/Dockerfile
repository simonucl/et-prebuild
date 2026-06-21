FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial repository state expected by the grading tests
RUN mkdir -p /home/user/db-backup

# version.txt with trailing newline
RUN echo '1.2.3' > /home/user/db-backup/version.txt

# CHANGELOG.md with trailing newline
RUN cat <<'EOF' > /home/user/db-backup/CHANGELOG.md
## [1.2.3] - 2023-09-10
### Fixed
- Corrected cron schedule for nightly backups
EOF
RUN echo >> /home/user/db-backup/CHANGELOG.md

# Permissions
RUN chmod a+rwx /home/user && \
    chmod -R a+rwX /home/user/db-backup

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

# From %environment
RUN chmod 755 /home/user