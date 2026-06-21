FROM ubuntu:22.04

# Help information:
# This image provides the initial filesystem state for the
# "storage audit" exercise.  It contains a directory tree in
# /home/user/storage_samples with files of specific sizes that
# pytest will verify.  Pytest is pre-installed so learners can
# run the provided test suite.

# ------------------------------------------------------------------
# Basic tools & Python testing framework
# ------------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Directory structure for the storage-audit exercise
# ------------------------------------------------------------------
# Ensure /home/user exists and is writable by any non-root user who
# will be running inside the container.
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Storage samples directory tree
RUN mkdir -p /home/user/storage_samples/docs && \
    mkdir -p /home/user/storage_samples/images

# Optional (but convenient) target directory the learner will write to
RUN mkdir -p /home/user/storage_audit && \
    chmod 0777 /home/user/storage_audit

# ------------------------------------------------------------------
# Create the files with exact byte sizes specified in the exercise
# ------------------------------------------------------------------
# 1. large_video.bin — 5 MiB (5 × 1 048 576)
RUN dd if=/dev/zero of=/home/user/storage_samples/large_video.bin bs=1M count=5 status=none

# 2. archive.tar.gz — 3 MiB
RUN dd if=/dev/zero of=/home/user/storage_samples/archive.tar.gz bs=1M count=3 status=none

# 3. docs/report.txt — 10 KiB
RUN dd if=/dev/zero of=/home/user/storage_samples/docs/report.txt bs=1K count=10 status=none

# 4. docs/data.csv — 15 KiB
RUN dd if=/dev/zero of=/home/user/storage_samples/docs/data.csv bs=1K count=15 status=none

# 5. images/photo1.jpg — exactly 1 MiB (threshold file)
RUN dd if=/dev/zero of=/home/user/storage_samples/images/photo1.jpg bs=1M count=1 status=none

# 6. images/photo2.jpg — 1.5 MiB (1 572 864 bytes)
RUN dd if=/dev/zero of=/home/user/storage_samples/images/photo2.jpg bs=1K count=1536 status=none

# 7. README.md — 512 bytes
RUN dd if=/dev/zero of=/home/user/storage_samples/README.md bs=512 count=1 status=none

# ------------------------------------------------------------------
# Permissions: world-readable to satisfy the tests & learners
# ------------------------------------------------------------------
RUN chmod -R a+r /home/user/storage_samples && \
    chmod 755 /home/user

WORKDIR /home/user