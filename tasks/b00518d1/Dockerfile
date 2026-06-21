# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: Automated Setup
# Description: Sets up the raw TSV data and installs pytest for the ML-pipeline exercise.
# This container image provides the starting filesystem state for the
# “ML pipeline / column extraction” task. It pre-loads two TAB-separated
# raw data files under /home/user/ml_pipeline/raw and installs pytest so
# that the grading harness can verify the initial state.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/ml_pipeline/raw && \
    chmod 755 /home/user /home/user/ml_pipeline /home/user/ml_pipeline/raw || true

RUN printf "event_id\tuser_id\ttimestamp\tevent_type\n""1\t1001\t2023-05-01T12:00:00Z\tclick\n""2\t1002\t2023-05-01T12:05:00Z\tview\n""3\t1003\t2023-05-01T12:10:00Z\tpurchase\n""4\t1004\t2023-05-01T12:20:00Z\tclick\n""5\t1005\t2023-05-01T12:25:00Z\tpurchase\n" \
    > /home/user/ml_pipeline/raw/user_events_part1.tsv

RUN printf "event_id\tcountry\tdevice\trevenue\n""1\tUS\tmobile\t0.00\n""2\tCA\tdesktop\t0.00\n""3\tUS\tmobile\t19.99\n""4\tGB\ttablet\t0.00\n""5\tCA\tmobile\t25.50\n" \
    > /home/user/ml_pipeline/raw/user_events_part2.tsv

RUN chmod 644 /home/user/ml_pipeline/raw/user_events_part1.tsv && \
    chmod 644 /home/user/ml_pipeline/raw/user_events_part2.tsv