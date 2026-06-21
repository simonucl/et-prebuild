FROM ubuntu:22.04

# Labels
LABEL Author="BackupExercise"
LABEL Description="Container image for integrity-check exercise – initial state only."

# Help documentation (as comments):
# This container provides the starting filesystem layout for the
# "backup integrity verification" exercise. All expected data files
# and the MD5 manifest are pre-installed under /home/user.
# No integrity report exists yet; participants must create it.

# Update package index and install Python + pip
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading test-suite
RUN pip3 install --no-cache-dir pytest

# Create the required directory structure
RUN mkdir -p /home/user/data_cluster/node1 && \
    mkdir -p /home/user/data_cluster/node2 && \
    mkdir -p /home/user/data_cluster/node3 && \
    mkdir -p /home/user/backup_manifests

# Data files (contents have NO trailing newline)
RUN printf 'foo'   > /home/user/data_cluster/node1/users.db && \
    printf 'bar'   > /home/user/data_cluster/node2/transactions.db && \
    printf 'hello' > /home/user/data_cluster/node2/corrupt.txt && \
    printf 'baz'   > /home/user/data_cluster/node3/logs.log

# Shipping manifest (relative paths exactly as expected)
RUN cat << 'EOF' > /home/user/backup_manifests/daily_20240515.md5
acbd18db4cc2f85cedef654fccc4a4d8  node1/users.db
37b51d194a7513e45b56f6524f2d51f2  node2/transactions.db
73feffa4b7f6bb68e44cf984c85f6e88  node3/logs.log
acbd18db4cc2f85cedef654fccc4a4d8  node2/corrupt.txt
EOF

# Permissions: readable by everyone, writable by the running user overlay
RUN chmod 0755 /home/user && \
    chmod -R 0755 /home/user/data_cluster && \
    chmod -R 0755 /home/user/backup_manifests && \
    chmod 0644 /home/user/data_cluster/node1/users.db && \
    chmod 0644 /home/user/data_cluster/node2/transactions.db && \
    chmod 0644 /home/user/data_cluster/node2/corrupt.txt && \
    chmod 0644 /home/user/data_cluster/node3/logs.log && \
    chmod 0644 /home/user/backup_manifests/daily_20240515.md5

# Explicitly make sure NO integrity_reports directory exists yet
RUN rm -rf /home/user/integrity_reports || true

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin

WORKDIR /home/user