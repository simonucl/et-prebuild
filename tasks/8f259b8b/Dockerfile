FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directories and placeholder files
RUN set -e && \
    ARTIFACT_RELEASE_DIR="/home/user/artifact_storage/releases" && \
    ARTIFACT_INDEX_DIR="/home/user/artifact_manager/index" && \
    ARTIFACT_DEBUG_DIR="/home/user/artifact_manager/debug" && \
    mkdir -p "$ARTIFACT_RELEASE_DIR" "$ARTIFACT_INDEX_DIR" "$ARTIFACT_DEBUG_DIR" && \
    touch "$ARTIFACT_RELEASE_DIR/appserver-2.4.1.bin" && \
    touch "$ARTIFACT_RELEASE_DIR/dbdriver-1.3.0.bin" && \
    touch "$ARTIFACT_RELEASE_DIR/utils-0.9.8.bin" && \
    printf 'appserver-2.4.1.bin\ndbdriver-1.3.0.bin\n' > "$ARTIFACT_INDEX_DIR/repository.index" && \
    chmod 0755 "$ARTIFACT_RELEASE_DIR" "$ARTIFACT_INDEX_DIR" "$ARTIFACT_DEBUG_DIR" && \
    chmod 0644 "$ARTIFACT_RELEASE_DIR/"*.bin "$ARTIFACT_INDEX_DIR/repository.index"

# Ensure /home/user exists and permissions
RUN mkdir -p /home/user && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8