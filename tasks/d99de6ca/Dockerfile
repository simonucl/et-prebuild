FROM ubuntu:22.04

RUN set -eux && \
    # Update package index and install Python + pip
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip pytest

# Create initial directory structure and seed files for the exercise
RUN set -eux && \
    # Base paths
    SRC_ROOT="/home/user/projects/local_workspace" && \
    NESTED_DIR="${SRC_ROOT}/nested" && \
    LOG_DIR="/home/user/sync_logs" && \
    # Create directories
    mkdir -p "${NESTED_DIR}" && \
    mkdir -p "${LOG_DIR}" && \
    # Create the three source files with exact byte contents
    printf "test"  > "${SRC_ROOT}/file1.txt" && \
    printf "hello" > "${SRC_ROOT}/file2.txt" && \
    printf "bye"   > "${NESTED_DIR}/info.txt" && \
    # Ensure /home/user/sync_logs is writable by any user
    chmod 777 "${LOG_DIR}" && \
    # Make sure all parent directories are at least readable/traversable
    chmod -R a+rx /home/user && \
    # The workspace itself only needs read/execute; leave as-is but ensure readability
    chmod -R a+rX "${SRC_ROOT}" && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8