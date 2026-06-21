FROM ubuntu:22.04

# Update package list and install Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-privileged user `user` with home directory /home/user
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi

# Ensure pip is up-to-date and install pytest for the grading harness
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest==7.4.0

# Set permissions on home directory
RUN chmod 755 /home/user

# Keep a sensible PATH; do NOT override $HOME
ENV PATH="/usr/local/bin:/usr/bin:/bin"

ENTRYPOINT []
CMD ["/bin/bash"]