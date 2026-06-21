FROM ubuntu:22.04

# Help/labels from %labels
LABEL Author="Container build for backup-engineer task"
LABEL Description="Provides pre-populated /home/user/production_data directory plus pytest"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/production_data/docs && \
    mkdir -p /home/user/production_data/images && \
    mkdir -p /home/user/production_data/config && \
    echo "Daily sales report" > /home/user/production_data/docs/report.txt && \
    echo "PNG_PLACEHOLDER" > /home/user/production_data/images/logo.png && \
    printf 'env=prod\nversion=1.2.0\n' > /home/user/production_data/config/app.conf && \
    printf 'host=localhost\nport=5432\n' > /home/user/production_data/config/db.conf && \
    chmod -R 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*