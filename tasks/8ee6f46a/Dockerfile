FROM ubuntu:22.04

# Author restore-config exercise setup
LABEL Author="restore-config exercise setup"

# This container image provides the pristine starting state for the
# “restore-config” exercise. It contains the compressed configuration
# snapshot at /home/user/restore_test/backup_config.tar.gz and has
# pytest pre-installed for automated grading.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip tar && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/restore_test && \
    chmod 755 /home/user

RUN mkdir -p /tmp/build_restore/restore_snapshot/etc && \
    printf "UTC\n" > /tmp/build_restore/restore_snapshot/etc/timezone && \
    printf "LANG=fr_FR.UTF-8\n" > /tmp/build_restore/restore_snapshot/etc/locale.conf

RUN tar -C /tmp/build_restore -czf /home/user/restore_test/backup_config.tar.gz restore_snapshot

RUN rm -rf /tmp/build_restore

RUN chmod -R u=rwX,go=rX /home/user/restore_test