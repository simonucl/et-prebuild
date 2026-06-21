# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text
# This Apptainer image provides the initial repository layout required for
# the “artifact-manager” auditing exercise. It pre-installs Python 3 and
# pytest and prepares the exact file hierarchy (with correct sizes and
# timestamps) under /home/user/repositories that the test-suite expects.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        coreutils \
        findutils && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/repositories/repoA/nested && \
    mkdir -p /home/user/repositories/repoB

# repoA files
RUN dd if=/dev/zero of=/home/user/repositories/repoA/oldlib-1.0.jar bs=31 count=1 status=none && \
    dd if=/dev/zero of=/home/user/repositories/repoA/newlib-2.0.jar bs=31 count=1 status=none && \
    dd if=/dev/zero of=/home/user/repositories/repoA/package-1.0.tar.gz bs=38 count=1 status=none && \
    truncate -s 0 /home/user/repositories/repoA/empty.tmp

# repoA/nested files
RUN dd if=/dev/zero of=/home/user/repositories/repoA/nested/legacy-0.9.jar bs=18 count=1 status=none && \
    dd if=/dev/zero of=/home/user/repositories/repoA/nested/sample-archive.tar.gz bs=36 count=1 status=none && \
    truncate -s 0 /home/user/repositories/repoA/nested/zero.txt

# repoB files
RUN dd if=/dev/zero of=/home/user/repositories/repoB/obsolete-2.3.jar bs=28 count=1 status=none && \
    dd if=/dev/zero of=/home/user/repositories/repoB/data-1.1.tar.gz bs=27 count=1 status=none && \
    truncate -s 0 /home/user/repositories/repoB/nothing.txt

# Set modification times
RUN touch -d "2020-01-01 00:00:00" /home/user/repositories/repoA/oldlib-1.0.jar && \
    touch -d "2020-02-01 00:00:00" /home/user/repositories/repoA/nested/legacy-0.9.jar && \
    touch -d "2019-12-01 00:00:00" /home/user/repositories/repoB/obsolete-2.3.jar && \
    touch -d "10 days ago" /home/user/repositories/repoA/nested/sample-archive.tar.gz && \
    touch -d "20 days ago" /home/user/repositories/repoB/data-1.1.tar.gz

# Relax permissions
RUN chmod -R a+rwX /home/user

# Labels
LABEL Author="artifact-manager bootstrap"