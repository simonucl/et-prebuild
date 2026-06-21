# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# From %help and %labels
# Author: Apptainer Task Preparer
# Description: Container providing initial state for Grafana dashboard frequency task, plus pytest.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip python3-setuptools python3-wheel && \
    pip3 install --no-cache-dir pytest

# Seed data
RUN mkdir -p /opt/seed
RUN cat <<'EOF' > /opt/seed/dashboard_hits.log
dashboard_cpu
dashboard_memory
dashboard_cpu
dashboard_cpu
dashboard_network
dashboard_memory
dashboard_disk
dashboard_network
dashboard_network
dashboard_disk
EOF
RUN chmod 0644 /opt/seed/dashboard_hits.log

# Prepare /home/user
RUN mkdir -p /home/user && chmod 0777 /home/user

# Prepare metrics directory and copy seeded log
RUN mkdir -p /home/user/metrics && \
    cp /opt/seed/dashboard_hits.log /home/user/metrics/dashboard_hits.log && \
    chmod 0644 /home/user/metrics/dashboard_hits.log && \
    chmod 755 /home/user

# Clean up
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"