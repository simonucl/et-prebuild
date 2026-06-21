# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author="Apptainer auto-setup for FinOps cost summary task"
LABEL Author="Apptainer auto-setup for FinOps cost summary task"

# Update APT and install Python & pip, then install pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem layout for FinOps exercise
RUN mkdir -p /home/user/cloud_logs && \
    chmod 0777 /home/user/cloud_logs

# September 2023 log
RUN cat <<'EOF' > /home/user/cloud_logs/usage-2023-09.csv
resource_id,service,usage_hours,cost
r1,Compute Engine,720,96.00
r2,Cloud Storage,5000,25.00
r3,BigQuery,100,150.00
r4,Compute Engine,100,13.33
r5,Cloud SQL,200,90.00
r6,Cloud Storage,3000,15.00
EOF

# October 2023 log
RUN cat <<'EOF' > /home/user/cloud_logs/usage-2023-10.csv
resource_id,service,usage_hours,cost
r1,Compute Engine,744,99.20
r2,Cloud Storage,5500,27.50
r3,BigQuery,90,135.00
r4,Compute Engine,120,16.00
r7,Cloud Functions,1000000,5.00
r6,Cloud Storage,3500,17.50
EOF

# Set permissions on CSV logs and home directory
RUN chmod 0644 /home/user/cloud_logs/usage-2023-09.csv && \
    chmod 0644 /home/user/cloud_logs/usage-2023-10.csv && \
    chmod 0755 /home/user

# Ensure Python and user binaries are on PATH
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH