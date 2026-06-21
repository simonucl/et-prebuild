# syntax=docker/dockerfile:1
# Container pre-configured for the “disk-usage summary” task.
# The directory /home/user/vuln_scans already contains three scan files.
# Students must create /home/user/scan_usage.log as instructed.
# Pytest is installed for automated grading.

FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/vuln_scans && \
    chmod 0755 /home/user/vuln_scans && \
    printf 'AAAA\n'  > /home/user/vuln_scans/scan1.nmap && \
    printf 'BBBBB\n' > /home/user/vuln_scans/scan2.nmap && \
    printf 'CCCCC\n' > /home/user/vuln_scans/errors.log && \
    chmod 0644 /home/user/vuln_scans/scan1.nmap && \
    chmod 0644 /home/user/vuln_scans/scan2.nmap && \
    chmod 0644 /home/user/vuln_scans/errors.log

RUN chmod 755 /home/user