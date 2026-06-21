FROM ubuntu:22.04

# Labels
LABEL Author="TaskSetup"
LABEL Description="Initial container state for the UTF-8 → Latin-1 conversion assignment"

# Base tools and Python/pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip locales ca-certificates && \
    sed -i 's/^# *en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare directory tree
RUN INSTALL_DIR="/home/user/project/pipelines/mobile" && \
    mkdir -p "${INSTALL_DIR}" && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/project && \
    chmod 0777 /home/user/project/pipelines && \
    chmod 0777 "${INSTALL_DIR}"

# Create the UTF-8 source file with the exact required contents (97 bytes)
RUN cat > /home/user/project/pipelines/mobile/build-notes-utf8.txt <<'EOF'
Release: 1.2.3
Changelog: Fixed résumé parsing, improved UI for Zürich
Author: José Álvarez
EOF

# Sanity-check byte size and set permissions
RUN INSTALL_DIR="/home/user/project/pipelines/mobile" && \
    BYTES=$(wc -c < "${INSTALL_DIR}/build-notes-utf8.txt") && \
    if [ "${BYTES}" -ne 97 ]; then \
        echo "build-notes-utf8.txt is ${BYTES} bytes, expected 97." >&2; \
        exit 1; \
    fi && \
    chmod 0644 "${INSTALL_DIR}/build-notes-utf8.txt"

# Environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8