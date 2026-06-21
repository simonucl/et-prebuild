# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help:
# This container provides the starting environment for the
# capacity-planning TSV trimming task. It includes:
# - The initial fixture file at /home/user/data/usage_report.tsv
# - Python 3 with pytest pre-installed for automated grading

LABEL Author="capacity-planning-exercise"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/data

RUN printf 'Timestamp\tServerID\tCPU_Usage\tMem_Usage\tDisk_Usage\tNetwork_In\tNetwork_Out\n' \
        > /home/user/data/usage_report.tsv && \
    printf '2023-07-01T00:15:00Z\tsrv-001\t52.5\t68.2\t70.1\t120.4\t98.6\n' \
        >> /home/user/data/usage_report.tsv && \
    printf '2023-07-01T00:15:00Z\tsrv-002\t33.0\t44.5\t60.0\t80.2\t60.0\n' \
        >> /home/user/data/usage_report.tsv && \
    printf '2023-07-01T00:15:00Z\tsrv-003\t85.2\t90.1\t88.5\t200.1\t150.2\n' \
        >> /home/user/data/usage_report.tsv && \
    printf '2023-07-01T00:15:00Z\tsrv-004\t10.5\t25.3\t30.5\t40.4\t30.1\n' \
        >> /home/user/data/usage_report.tsv && \
    printf '2023-07-01T00:15:00Z\tsrv-005\t67.7\t75.0\t79.2\t130.2\t110.7\n' \
        >> /home/user/data/usage_report.tsv

RUN chmod 0644 /home/user/data/usage_report.tsv && \
    chmod 0755 /home/user /home/user/data