FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create non-root user `user`
RUN useradd -m -s /bin/bash user

# Build directory structure
RUN mkdir -p /home/user/remote_server/etc && \
    mkdir -p /home/user/new_creds

# Populate the old credentials file
RUN cat <<'EOF' > /home/user/remote_server/etc/credentials.txt
username: admin
password: OldP@ssw0rd!
EOF

# Populate the new credentials file
RUN cat <<'EOF' > /home/user/new_creds/credentials.txt
username: admin
password: N3wSecur3P@ss!
EOF

# Set ownership and permissions
RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/remote_server /home/user/remote_server/etc /home/user/new_creds && \
    chmod 644 /home/user/remote_server/etc/credentials.txt /home/user/new_creds/credentials.txt

# Environment variables
ENV PYTHONIOENCODING=utf-8
ENV LC_ALL=C.UTF-8