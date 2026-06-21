FROM ubuntu:22.04

# Install system packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata \
        jq \
        gnupg \
        tar \
        gzip \
        coreutils && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness
RUN pip3 install --no-cache-dir pytest

# Prepare the directory tree expected by the assignment
RUN mkdir -p /home/user/data

# Create the pre-existing CSV file with strict contents
RUN cat > /home/user/data/db_backups_2023.csv <<'EOF'
database,last_backup,size_mb
customers,2023-11-15T14:03:00Z,512
orders,2023-10-01T02:11:00Z,256
inventory,2023-11-29T05:45:00Z,128
analytics,2023-09-20T00:00:00Z,2048
sessions,2023-11-30T12:00:00Z,64
EOF

# Ensure correct permissions
RUN chmod 0644 /home/user/data/db_backups_2023.csv && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/data

# Set environment variables
ENV PATH=/usr/local/bin:$PATH

# Set working directory
WORKDIR /home/user

CMD ["echo", "Container for the Database Backup Reporting assignment. Use an interactive shell to work on the task."]