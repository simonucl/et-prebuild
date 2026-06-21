FROM ubuntu:22.04

# Ensure package list is up-to-date and required tools are present
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates \
        build-essential && \
    # Install pytest for the test harness
    pip3 install --no-cache-dir pytest && \
    # Create a writable home for the "user" account expected by the tests
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Convenience symlink so `python` resolves to `python3`
    ln -sf /usr/bin/python3 /usr/local/bin/python || true && \
    # Clean up APT caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Minimal environment – do NOT override $HOME
ENV LC_ALL=C
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin
ENV HOME=/home/user

WORKDIR /home/user

CMD ["echo", "Container ready. Start solving the assignment inside /home/user."]