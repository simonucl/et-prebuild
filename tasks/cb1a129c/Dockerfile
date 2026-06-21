FROM ubuntu:22.04

# Labels
LABEL Author="FileSyncTaskBuilder"
LABEL Description="Container with initial state for the file-synchronisation task and pytest installed."

RUN set -eux && \
    # Update package index and install required software
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip rsync && \
    # Install pytest for the assessment framework
    pip3 install --no-cache-dir pytest && \
    # -----------------------------------------------------------------
    # Prepare initial filesystem state expected by the test-suite
    # -----------------------------------------------------------------
    # Create base directories with the required permissions
    mkdir -p /home/user/incoming && \
    mkdir -p /home/user/remote_backup && \
    chmod 755 /home/user && \
    chmod 755 /home/user/incoming && \
    chmod 755 /home/user/remote_backup && \
    # Populate /home/user/incoming with the prescribed files
    printf 'Quarterly data\n' > /home/user/incoming/report.txt && \
    printf 'PNG' > /home/user/incoming/image.png && \
    chmod 644 /home/user/incoming/report.txt /home/user/incoming/image.png && \
    # Clean up apt caches to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Ensure user-land Python tools are reachable
ENV PATH=/usr/local/bin:$PATH