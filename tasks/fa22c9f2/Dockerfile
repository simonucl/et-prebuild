FROM ubuntu:22.04

# Help:
# Container image pre-configured for the “checksum verification” task.
# It contains:
#   • Project skeleton in /home/user/project
#   • pytest installed for grading
# Author="Apptainer Setup Script for Checksum Verification Exercise"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN PROJECT_ROOT="/home/user/project" && \
    ASSETS_DIR="${PROJECT_ROOT}/assets" && \
    CHECKSUMS_DIR="${PROJECT_ROOT}/checksums" && \
    mkdir -p "${ASSETS_DIR}" "${CHECKSUMS_DIR}" && \
    : > "${ASSETS_DIR}/blank.js" && \
    echo "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  assets/blank.js" \
        > "${CHECKSUMS_DIR}/sha256sums.txt"

RUN chmod 755 /home /home/user && \
    chmod 755 /home/user/project /home/user/project/assets /home/user/project/checksums && \
    chmod 644 /home/user/project/assets/blank.js /home/user/project/checksums/sha256sums.txt

ENV LC_ALL=C
ENV PATH=/usr/local/bin:/usr/bin:/bin