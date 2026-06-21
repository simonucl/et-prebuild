FROM ubuntu:22.04

# Help:
# This container provides the tools required for the SQLite diagnostics
# bundle exercise:
#   - sqlite3 CLI
#   - Python 3 and pytest for automated testing
# It intentionally does not contain the /home/user/diagnostics directory
# so that learners can create it during the task.

LABEL Author="Apptainer Build Script"
LABEL Description="Environment for SQLite diagnostics bundle exercise with pytest installed."

ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user