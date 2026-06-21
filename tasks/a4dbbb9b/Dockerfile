FROM ubuntu:22.04

# Base utilities
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/.secrets && \
    printf 'OLD_KEY_PLACEHOLDER\n' > /home/user/.secrets/old_key.pem && \
    printf 'NEW_KEY_PLACEHOLDER\n' > /home/user/.secrets/new_key.pem && \
    ln -sf /home/user/.secrets/old_key.pem /home/user/.secrets/active_key.pem && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/.secrets

# Environment variables (chmod cannot be in ENV — moved above)
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8