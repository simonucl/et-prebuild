# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Cloud-Costs-Exercise"
LABEL Description="Baseline container for the FinOps Makefile exercise"

# This container seeds the workspace with raw cloud-cost CSV files and an empty
# output directory. pytest is pre-installed for automated grading.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        make && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create the required directory structure
RUN mkdir -p /home/user/cloud-costs/raw && \
    mkdir -p /home/user/cloud-costs/output

# Populate the raw CSV files with the exact contents expected by the tests
RUN cat > /home/user/cloud-costs/raw/aws_costs.csv <<'EOF'
service,cost,month
EC2,23.50,2023-06
S3,30.70,2023-06
EOF

RUN cat > /home/user/cloud-costs/raw/gcp_costs.csv <<'EOF'
service,cost,month
ComputeEngine,15.30,2023-06
CloudStorage,14.50,2023-06
EOF

RUN cat > /home/user/cloud-costs/raw/azure_costs.csv <<'EOF'
service,cost,month
VM,20.00,2023-06
BlobStorage,21.00,2023-06
EOF

# Ensure correct permissions so the non-root agent can read/write
RUN chmod 755 /home/user /home/user/cloud-costs /home/user/cloud-costs/raw /home/user/cloud-costs/output && \
    chmod 644 /home/user/cloud-costs/raw/*.csv