FROM ubuntu:22.04

# Install system packages and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Create initial filesystem expected by the tests
# Create user home directory tree
RUN mkdir -p /home/user/db && \
    mkdir -p /home/user/logs && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/db && \
    chmod 0755 /home/user/logs

# Create the initial PostgreSQL configuration file
RUN cat >/home/user/db/postgresql.conf <<'EOF'
# PostgreSQL configuration file
# Memory settings
work_mem = 4MB
# End
EOF

# Set correct permissions for the configuration file
RUN chmod 0644 /home/user/db/postgresql.conf

# Environment variables
ENV PATH="$PATH:/home/user"

WORKDIR /home/user

CMD ["/bin/bash"]