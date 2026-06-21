FROM ubuntu:22.04

# Author AgentPreparation
# Description "Container for FinOps JSON compression task – sets up initial filesystem state and installs pytest."
LABEL Author="AgentPreparation" Description="Container for FinOps JSON compression task – sets up initial filesystem state and installs pytest."

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates coreutils findutils gzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    mkdir -p /home/user/cloud_costs/raw_usage && \
    chmod 700 /home/user/cloud_costs && \
    chmod 700 /home/user/cloud_costs/raw_usage && \
    truncate -s 2097152  /home/user/cloud_costs/raw_usage/2023-11-01-usage.json && \
    truncate -s 3145728  /home/user/cloud_costs/raw_usage/2024-01-01-usage.json && \
    truncate -s 1245184  /home/user/cloud_costs/raw_usage/2024-01-15-usage.json && \
    truncate -s 512000   /home/user/cloud_costs/raw_usage/2023-12-01-usage.json && \
    rm -f /home/user/cloud_costs/compression_report.csv

# From %environment
RUN chmod 755 /home/user

ENV PYTHONIOENCODING="utf-8"
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# From %runscript
# This container is prepared for the FinOps JSON compression task.
# Run your commands inside the container as needed.