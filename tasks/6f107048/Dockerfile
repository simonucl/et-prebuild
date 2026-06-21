# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: DB-Optimisation-Exercise
# Description: Environment with initial CSV fixtures for DB optimisation reporting task.

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Updating APT and installing Python tooling..." && \
    apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating data directory structure and CSV fixtures..." && \
    mkdir -p /home/user/data

RUN cat >/home/user/data/query_stats_2023.csv <<'EOF'
query_id,db,timestamp,exec_time_ms,cpu_ms,io_reads
Q1,db1,2023-06-15T10:15:30,120,80,200
Q2,db2,2023-07-20T11:30:00,250,150,300
Q3,db1,2023-08-05T09:45:10,90,60,100
Q4,db2,2023-09-12T14:20:05,310,200,400
EOF

RUN cat >/home/user/data/query_stats_2024.csv <<'EOF'
query_id,db,timestamp,exec_time_ms,cpu_ms,io_reads
Q1,db1,2024-01-18T12:10:20,110,70,190
Q5,db2,2024-02-25T15:40:00,340,220,450
Q6,db1,2024-03-03T08:05:55,95,65,110
Q7,db2,2024-04-10T16:25:30,280,180,350
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 644 /home/user/data/query_stats_2023.csv && \
    chmod 644 /home/user/data/query_stats_2024.csv && \
    echo "Container setup complete."

# This container image provides the initial filesystem state required for the
# “DB optimisation report” exercise. Two CSV files are pre-populated under
# /home/user/data/, and pytest is installed for automated grading.