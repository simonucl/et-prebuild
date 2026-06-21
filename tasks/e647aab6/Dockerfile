FROM ubuntu:22.04

# Container for the "tiny local artifact catalogue in SQLite" exercise.
#
# Includes:
#   • sqlite3 CLI
#   • Python 3
#   • pytest
#
# A non-root user "user" with home directory /home/user is pre-created.
# No exercise artefacts (directory, database, CSV, or log) are present yet,
# leaving a clean slate for students to work on the task.

# Base tooling
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    # Python testing framework
    pip3 install --no-cache-dir pytest && \
    # Non-root working user
    useradd -m -s /bin/bash user && \
    chown -R user:user /home/user && \
    chmod 755 /home/user && \
    # Clean up APT caches to keep image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make sure /usr/local/bin (where pip installs executables) is on PATH.
ENV PATH="/usr/local/bin:$PATH"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8