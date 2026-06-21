FROM ubuntu:22.04

# Install Python and pytest
RUN set -eux; \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create non-root user `user`
RUN set -eux; \
    if ! getent group 1000 >/dev/null; then groupadd -g 1000 user; fi && \
    if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -g 1000 -s /bin/bash user; fi

# Set up the initial directory structure and script required by the tests
RUN set -eux; \
    mkdir -p /home/user/ml_training/bin

RUN cat <<'EOF' > /home/user/ml_training/bin/prepare_data.sh
#!/usr/bin/env bash
echo "Preparing data"
EOF

RUN chmod +x /home/user/ml_training/bin/prepare_data.sh

# Ensure ownership belongs to the non-root user
RUN chown -R 1000:1000 /home/user/ml_training

# Fix /home/user permissions
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH