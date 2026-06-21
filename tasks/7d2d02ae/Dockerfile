FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user `user`
RUN useradd -m -u 1000 -s /bin/bash user

# Set up the required directory structure and empty CSV stubs
RUN DATASET_BASE="/home/user/datasets" && \
    mkdir -p "${DATASET_BASE}/raw_data" "${DATASET_BASE}/processed_data" && \
    touch "${DATASET_BASE}/raw_data/dataset_node1.csv" \
          "${DATASET_BASE}/raw_data/dataset_node2.csv" \
          "${DATASET_BASE}/raw_data/dataset_node3.csv" && \
    chown -R user:user /home/user

# Commands from %environment that are not env vars
RUN chmod 755 /home/user

# Environment variables from %environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH