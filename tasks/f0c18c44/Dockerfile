FROM ubuntu:22.04

RUN set -e && \
    # Minimal OS packages for Python development and virtual environments
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    # Install pytest for the test harness
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    # Create an accessible workspace for the student
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up apt cache to keep image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user

ENTRYPOINT ["sh", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]