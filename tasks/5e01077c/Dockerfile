# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# System packages
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Python testing framework
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial filesystem state for the exercise
# ------------------------------------------------------------------
RUN mkdir -p /home/user/cloud_migration && \
    chmod 777 /home/user /home/user/cloud_migration

RUN cat >/home/user/cloud_migration/full_system.log <<'EOF'
[2023-10-01 08:10:16] [INFO] [auth-service] User login successful userId=23
[2023-10-01 08:10:18] [WARN] [gateway] High latency detected route=/api/payments
[2023-10-01 08:10:20] [ERROR] [db-service] Connection timeout to primary replica
[2023-10-01 08:11:05] [INFO] [billing-service] Invoice generated invoiceId=9821
[2023-10-01 08:12:45] [CRITICAL] [db-service] Data corruption detected segment=alpha
[2023-10-01 08:13:02] [ERROR] [cache-service] Redis cluster unreachable
[2023-10-01 08:14:33] [INFO] [db-service] Background vacuum completed table=orders
[2023-10-01 08:15:14] [WARN] [auth-service] Suspicious login attempt userId=88
[2023-10-01 08:16:29] [ERROR] [db-service] Failed to apply migration file V23__add_index.sql
[2023-10-01 08:17:42] [INFO] [gateway] Deployment finished version=1.3.4
EOF

# Ensure the log file has expected permissions
RUN chmod 666 /home/user/cloud_migration/full_system.log

# ------------------------------------------------------------------
# Environment configuration
# ------------------------------------------------------------------
RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

# ------------------------------------------------------------------
# Metadata
# ------------------------------------------------------------------
LABEL Author="Apptainer build script for cloud migration log-filter task"

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
# This container provides the initial state for the "cloud_migration" log-filter
# exercise. It includes:
#   • /home/user/cloud_migration/full_system.log  (10-line fixture)
#   • No /home/user/cloud_migration/alerts directory
# Python and pytest are preinstalled to run the automated assessment.