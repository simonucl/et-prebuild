FROM ubuntu:22.04

# Help / Labels
LABEL Author="backup-exercise-builder"
LABEL Description="Initial state for the restore exercise: backup archive present, pytest installed."

ENV PYTHONDONTWRITEBYTECODE=1

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-setuptools \
        ca-certificates coreutils tar gzip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/backups && \
    BUILD_DIR="$(mktemp -d)" && \
    mkdir -p "${BUILD_DIR}/etc/nginx/conf.d" && \
    mkdir -p "${BUILD_DIR}/var/www/html/assets" && \
    printf 'abcdefghijklmnopqrstuvwxyz' > "${BUILD_DIR}/etc/nginx/nginx.conf" && \
    printf 'abc' > "${BUILD_DIR}/etc/nginx/conf.d/default.conf" && \
    printf 'a' > "${BUILD_DIR}/var/www/html/index.html" && \
    : > "${BUILD_DIR}/var/www/html/healthcheck.php" && \
    printf 'message digest' > "${BUILD_DIR}/var/www/html/assets/style.css" && \
    tar -C "${BUILD_DIR}" -czf /home/user/backups/site_config_backup.tar.gz etc var && \
    rm -rf "${BUILD_DIR}" && \
    chmod -R a+rX /home/user && \
    chmod 755 /home/user