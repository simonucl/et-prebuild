# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install required packages and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial filesystem state for the coding task
# ------------------------------------------------------------------

# Create the /home/user hierarchy and set broad permissions
RUN mkdir -p /home/user/etl_data && \
    chmod 0777 /home/user

# Populate source data files exactly as described
RUN cat > /home/user/etl_data/customers.csv <<'EOF'
id,name
1,Alice
2,Bob
EOF

RUN cat > /home/user/etl_data/orders.csv <<'EOF'
order_id,customer_id,amount
1001,1,250.00
1002,2,150.00
EOF

RUN cat > /home/user/etl_data/readme.txt <<'EOF'
Sample ETL source data.
EOF

# Set appropriate permissions: readable by everyone, not writable
RUN chmod 0755 /home/user/etl_data && \
    chmod 0644 /home/user/etl_data/*

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="Apptainer Task Prep Bot"
LABEL Description="Container environment for ETL sync command-line task with pytest pre-installed."

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
# This container provides the initial filesystem state for the ETL synchronisation
# exercise. It includes:
#
#  • /home/user/etl_data with three source files.
#  • pytest pre-installed for the automated grading harness.
#
# The student’s task is to run a single command (no script) that copies the
# contents of /home/user/etl_data to /home/user/backup/etl_data while preserving
# timestamps and then writes an alphabetically-sorted list of the copied
# filenames to /home/user/etl_sync.log.