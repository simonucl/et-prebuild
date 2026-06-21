FROM ubuntu:22.04

# Basic tools and Python testing framework
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        pigz \
        time \
        ca-certificates \
        locales && \
    pip3 install --no-cache-dir pytest && \
    locale-gen en_US.UTF-8

# Create the normal user and its home directory
RUN if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user || true; \
        useradd -m -u 1000 -g 1000 -s /bin/bash user || true; \
    fi

# Prepare the source data directory
RUN mkdir -p /home/user/data_to_backup && \
    for i in $(seq 1 8); do \
        yes "Sample data for backup benchmark file $i" | head -c 1048576 > /home/user/data_to_backup/file${i}.txt; \
    done && \
    chown -R 1000:1000 /home/user

# Clean up APT caches
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment setup
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:${PATH}"

# Equivalent of runscript
CMD echo "Container for the 'backup benchmark' assignment." && \
    echo "Run your benchmark script inside this container as the normal user."