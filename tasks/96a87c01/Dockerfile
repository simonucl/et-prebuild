# syntax=docker/dockerfile:1
# This container supplies the starting filesystem state for the “SQL checksum
# verification” exercise. It pre-installs Python, pip, and pytest and ships an
# empty /home/user/db_exports/optimized_queries.sql file ready for the student
# to verify.

FROM ubuntu:22.04

LABEL Author="DB-Checksum-Task Build System"
LABEL Description="Base image providing the initial state for the SQL checksum verification assignment."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    mkdir -p /home/user/db_exports && \
    chmod 755 /home/user/db_exports && \
    : > /home/user/db_exports/optimized_queries.sql && \
    chmod 644 /home/user/db_exports/optimized_queries.sql