FROM ubuntu:22.04

# Labels
LABEL Author="Auto-generated container for backup task"
LABEL Description="Provides the initial state and dependencies for the backup exercise"

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        pigz \
        pbzip2 \
        bzip2 \
        xz-utils \
        tar \
        gzip \
        ca-certificates \
        git \
        coreutils && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the forthcoming test-suite
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create unprivileged user and its home directory
# Use UID 1000 (common default); if the runtime UID differs it will
# still be able to use /home/user because we open permissions later.
RUN useradd -m -u 1000 -s /bin/bash user || true

# Prepare initial directory tree and sample data files
RUN set -e && \
    BASE=/home/user && \
    DATA_DIR=${BASE}/data && \
    mkdir -p "${DATA_DIR}/projectA" "${DATA_DIR}/projectB" && \
    printf 'Annual Report 2023 final version\n' > "${DATA_DIR}/projectA/report.txt" && \
    printf 'temporary data\n' > "${DATA_DIR}/projectA/draft.tmp" && \
    printf '# sample configuration\nversion = 1.0\nenabled = true\n' > "${DATA_DIR}/projectB/config.cfg" && \
    printf 'Meeting notes for upcoming release\nRemember to update changelog.\n' > "${DATA_DIR}/projectB/notes.txt" && \
    chmod -R a+rwx /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["sh", "-c", "echo 'Container for backup-task exercises.' && echo 'Invoke your desired command inside the container as usual.'"]