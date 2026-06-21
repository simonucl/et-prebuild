FROM ubuntu:22.04

# Install Python and Pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial data set expected by the test harness
RUN mkdir -p /home/user/data_to_backup/images && \
    mkdir -p /home/user/data_to_backup/scripts && \
    printf 'First document\n' > /home/user/data_to_backup/doc1.txt && \
    dd if=/dev/urandom of=/home/user/data_to_backup/images/photo.jpg bs=1024 count=1 status=none && \
    printf '#!/bin/bash\necho backup\n' > /home/user/data_to_backup/scripts/backup.sh && \
    chmod +x /home/user/data_to_backup/scripts/backup.sh && \
    chmod -R a+rX /home/user

# From %environment
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8

# From %runscript
CMD echo "Apptainer image for the backup task." && echo "Navigate to /home/user and follow the instructions to create the backup bundle."