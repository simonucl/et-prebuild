FROM ubuntu:22.04

# Basic system utilities
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user && \
    mkdir -p /home/user/mock_api && \
    mkdir -p /home/user/compliance && \
    echo '{"status":"ok"}' > /home/user/mock_api/health.json && \
    chmod 0755 /home/user/mock_api && \
    chmod 0644 /home/user/mock_api/health.json && \
    chmod 0755 /home/user/compliance && \
    chown -R 1000:1000 /home/user/mock_api /home/user/compliance && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"

# Default entrypoint: open an interactive shell
CMD ["/bin/bash"]