# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="Container Prep Bot"
LABEL Description="Environment for gzip compression exercise with pytest pre-installed"

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Install required software and prepare filesystem
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gzip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/capacity && \
    chmod 755 /home/user && \
    chmod 755 /home/user/capacity

# Create the weekly_report.csv with the exact required content
RUN cat >/home/user/capacity/weekly_report.csv <<'EOF'
week,start,end,cpu_usage_pct,mem_usage_pct
23,2024-06-03,2024-06-09,57.3,62.1
24,2024-06-10,2024-06-16,59.8,63.7
25,2024-06-17,2024-06-23,61.2,65.4
26,2024-06-24,2024-06-30,60.0,64.0
EOF

# Ensure correct permissions on the CSV
RUN chmod 644 /home/user/capacity/weekly_report.csv

# This container provides the initial environment for the capacity-planning
# compression task. The file /home/user/capacity/weekly_report.csv is
# present; the student must create a valid gzip archive of it and print
# 'COMPRESSION DONE' as specified.