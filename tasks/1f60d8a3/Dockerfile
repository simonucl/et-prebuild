FROM ubuntu:22.04

# Labels
LABEL Author="benchmark-task-prep"
LABEL Description="Container image for simple compression-benchmark task. Provides Python, pytest and common compressors. Leaves /home/user clean so that the student can create the required artefacts during execution."

# Post installation
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        gzip \
        bzip2 \
        xz-utils \
        time \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Set working directory
WORKDIR /home/user

# Default entrypoint: just launch an interactive shell
CMD ["/bin/bash"]

# Help information (as comments):
# This image supplies:
#   • gzip, bzip2, xz compressors
#   • GNU time utility for simple benchmarking
#   • Python 3 + pytest for automated grading
#
# The workspace /home/user is empty and writable; the student will
# perform all tasks inside that directory.