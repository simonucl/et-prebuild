FROM ubuntu:22.04

# Labels
LABEL Maintainer="backoffice"
LABEL Description="Environment for archive-integrity task (pytest included)"

#---------------------------------------------------------------------------
# Basics and Python tooling
#---------------------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        gzip \
        ca-certificates \
        dpkg \
        coreutils && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#---------------------------------------------------------------------------
# Create an unprivileged user `user` with home /home/user
#---------------------------------------------------------------------------
RUN adduser --disabled-password --gecos "" user

#---------------------------------------------------------------------------
# Prepare required initial filesystem state
#  /home/user/archives/
#       ├── backup_20231015.tar.gz                (empty file, 0 bytes)
#       └── backup_20231015.tar.gz.sha256         (one-line reference hash)
#---------------------------------------------------------------------------
RUN ARCHIVE_DIR="/home/user/archives" && \
    mkdir -p "${ARCHIVE_DIR}" && \
    : > "${ARCHIVE_DIR}/backup_20231015.tar.gz" && \
    printf 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  backup_20231015.tar.gz\n' \
        > "${ARCHIVE_DIR}/backup_20231015.tar.gz.sha256" && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# This container image provides the starting environment for the
# archive-integrity verification task.  The necessary archive files are
# pre-installed under /home/user/archives, while the verify_logs directory
# is intentionally absent so that the learner can create it.  pytest is
# available for the automated grader.