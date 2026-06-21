FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Container for nightly backup confirmation task with pytest pre-installed."

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Basic development utilities
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tar && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare the directory layout expected by the grader
RUN mkdir -p /home/user/scripts && \
    mkdir -p /home/user/data/source_data && \
    mkdir -p /home/user/backups && \
    mkdir -p /home/user/logs

# Sample data so that the backup has something to package
RUN echo "example data" > /home/user/data/source_data/file1.txt

# Create the backup script
RUN cat << 'EOF' > /home/user/scripts/backup.sh
#!/usr/bin/env bash
# Simple simulated backup tool
# It copies /home/user/data/source_data into a tar.gz archive inside /home/user/backups.
set -e
dest="/home/user/backups/archive.tar.gz"
tar -czf "$dest" -C /home/user/data/source_data .
echo "Backup completed"
exit 0
EOF

RUN chmod 755 /home/user/scripts/backup.sh

# Permissions so the non-root runtime user can work freely
RUN chmod 755 /home/user/scripts && \
    chmod -R 755 /home/user/data && \
    chmod 777 /home/user/backups && \
    chmod 777 /home/user/logs

WORKDIR /home/user

CMD ["/bin/bash"]