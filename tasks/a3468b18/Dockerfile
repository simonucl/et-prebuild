FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Set up directories and initial project tree
RUN PROJECT_DIR="/home/user/project" && \
    DATA_DIR="${PROJECT_DIR}/data" && \
    mkdir -p "${DATA_DIR}" && \
    printf 'abc' > "${DATA_DIR}/file1.txt" && \
    printf 'The quick brown fox jumps over the lazy dog' > "${DATA_DIR}/file2.bin" && \
    rm -rf "${PROJECT_DIR}/checksums" && \
    chmod 777 "${PROJECT_DIR}" && \
    chmod 644 "${DATA_DIR}/file1.txt" "${DATA_DIR}/file2.bin" && \
    chmod 755 "${DATA_DIR}"

# Apply environment-time permissions (converted to RUN)
RUN chmod 755 /home/user

# Labels
LABEL Author="Checksum Manifest Setup"
LABEL Description="Container prepared for checksum-manifest exercise (pytest inside)"