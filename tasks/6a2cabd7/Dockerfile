# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %help
# This container provides the initial filesystem state and
# dependencies (Python, pytest) required for the SQL-backup clean-up task.
# The student will perform their work after this image is instantiated.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    echo "Updating package index and installing required packages..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        gzip \
        coreutils \
        --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip echo "Installing pytest..." && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    echo "Creating user 'user' with UID 1000 (if not already present)..." && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g 1000 user; \
    fi

RUN set -e && \
    echo "Setting up initial directory tree and files..." && \
    base=/home/user/db_migrations && \
    mkdir -p "${base}/2021" \
             "${base}/2022/temp" \
             "${base}/2023" \
             "${base}/legacy" && \
    create_file() { \
        path="$1"; \
        size="$2"; \
        dd if=/dev/zero of="${path}" bs=1 count="${size}" status=none; \
    }; \
    create_file "${base}/2021/01_schema_update.sql.bak"      1500 && \
    create_file "${base}/2021/02_index_update.sql.bak"        900 && \
    create_file "${base}/2022/03_add_columns.sql.bak"        3000 && \
    create_file "${base}/2022/temp/04_cleanup.sql.bak"       5000 && \
    create_file "${base}/2023/05_remove_obsolete.sql.bak"     800 && \
    create_file "${base}/legacy/06_legacy_patch.sql.bak"     2048

RUN set -e && \
    echo "Adjusting ownership and permissions so the non-root runtime user can work..." && \
    chown -R 1000:1000 /home/user && \
    chmod -R u+rwX,go+rX /home/user && \
    chmod 755 /home/user && \
    echo "Initial state ready."

LABEL Author="SQL-Backup-Cleanup-Prep" \
      Description="Container image prepared for the SQL-backup clean-up task"

USER user
WORKDIR /home/user