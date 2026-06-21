# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author capacity_planning_container_builder
# Description: Base container for capacity-planner symlink task – includes pytest and initial snapshot data.
# Help:
# This container provides the starting filesystem state for the capacity-planning
# symlink exercise. It includes:
#   /home/user/snapshots/{2023-06-01,2023-07-01}/{cpu.csv,memory.csv}
# The /home/user directory is world-writable so the unprivileged agent can create
# new files and directories as required by the assignment.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    for DATE in 2023-06-01 2023-07-01; do \
        mkdir -p /home/user/snapshots/${DATE}; \
        touch /home/user/snapshots/${DATE}/cpu.csv; \
        touch /home/user/snapshots/${DATE}/memory.csv; \
    done && \
    chmod -R a+rX /home/user

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:$PATH

LABEL Author="capacity_planning_container_builder"
LABEL Description="Base container for capacity-planner symlink task – includes pytest and initial snapshot data."