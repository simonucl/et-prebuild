FROM ubuntu:22.04

# Labels
LABEL Author="benchmark-setup"
LABEL Description="Initial filesystem and tooling for gzip timing benchmark task."

# Update apt cache and install required packages
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        gzip \
        time \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0755 /home /home/user && \
    mkdir -p /home/user/artifacts && \
    chmod 0755 /home/user/artifacts && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create the build artifact file (~11 KB) with placeholder content
RUN TAR_PATH="/home/user/artifacts/build_v1.2.3.tar" && \
    : > "${TAR_PATH}" && \
    for i in $(seq 1 700); do \
        echo "Hello Build Engineer" >> "${TAR_PATH}"; \
    done && \
    chmod 0644 "${TAR_PATH}"

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

WORKDIR /home/user

# Default command
CMD echo "Container ready for the gzip timing benchmark task." && echo "Refer to the assignment instructions for what actions to perform."

# Help:
# This container sets up the initial state for the gzip compression timing
# benchmark task. It pre-installs gzip, GNU time, and pytest, and provides the
# required build artifact under /home/user/artifacts/ with the correct
# permissions.