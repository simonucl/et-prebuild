# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Container Build Script"
LABEL Purpose="Environment for the Cluster Telemetry Trimming task"

# Install Python, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare the initial filesystem state required by the exercise
RUN mkdir -p /home/user/data

# Create the TSV input file
RUN cat > /home/user/data/cluster_resource_usage.tsv <<'EOF'
Timestamp	Node	CPU_Used	CPU_Total	Memory_Used	Memory_Total	Disk_Used	Disk_Total
2023-08-07T00:00:00Z	node01	45	64	32768	65536	120	250
2023-08-07T00:00:00Z	node02	53	64	41984	65536	140	250
2023-08-07T01:00:00Z	node01	47	64	33000	65536	121	250
2023-08-07T01:00:00Z	node02	52	64	42050	65536	141	250
2023-08-07T02:00:00Z	node01	49	64	33100	65536	122	250
EOF

# Set permissions so the non-root agent can read the data
RUN chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 644 /home/user/data/cluster_resource_usage.tsv

# Environment variables from Apptainer %environment
ENV PYTHONUNBUFFERED=1