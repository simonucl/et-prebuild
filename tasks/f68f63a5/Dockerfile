FROM ubuntu:22.04

# Help / metadata from %labels
LABEL Author="backup-integrity-setup"
LABEL Description="Container prepared for the Backup Verification task – includes test fixtures and pytest."

# Environment variables from %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Fix home permissions
RUN chmod 755 /home/user || true

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/backups/tmp && \
    printf "Hello backup\n" > /home/user/backups/tmp/hello.txt && \
    tar -C /home/user/backups/tmp -czf /home/user/backups/weekly_backup.tar.gz hello.txt && \
    rm -rf /home/user/backups/tmp && \
    HASH=$(sha256sum /home/user/backups/weekly_backup.tar.gz | awk '{print $1}') && \
    echo "${HASH}  weekly_backup.tar.gz" > /home/user/backups/expected_sha256.txt && \
    chmod -R a+rX /home/user/backups

ENTRYPOINT []