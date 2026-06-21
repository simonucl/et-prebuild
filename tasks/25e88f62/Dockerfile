FROM ubuntu:22.04

# Help: This container sets up a clean Ubuntu 22.04 environment with Python, pytest,
# and SQLite installed. A writable /home/user directory is prepared for the
# "artifact-manager" assignment, but no assignment artefacts are created yet.

RUN set -e && \
    echo "Updating package index and installing required packages…" && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    echo "Installing pytest via pip…" && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating writable /home/user directory (leave it otherwise empty)…" && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    echo "Providing a convenient 'python' symlink to python3…" && \
    ln -sf /usr/bin/python3 /usr/local/bin/python && \
    echo "Cleaning up apt caches…" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure pip-installed CLI tools are on PATH
ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /home/user

CMD ["/bin/bash"]