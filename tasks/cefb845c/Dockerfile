FROM ubuntu:22.04

# Author ExampleBuilder
# Description "Environment for disk-usage cleanup & report task"

# Help:
# This container image provides the exact starting filesystem state required
# for the "disk-usage cleanup & report" exercise.  Pytest is pre-installed so
# the automated grader can validate both the initial conditions and the
# student's final outcome.

# Update APT and install Python + pip
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Prepare the initial file hierarchy expected by the automated tests
# Base directories
RUN mkdir -p /home/user/workshop/data/raw && \
    mkdir -p /home/user/workshop/data/processed && \
    mkdir -p /home/user/workshop/data/extra

# Create the exact files with their required sizes (all null-bytes)
# raw/big_dataset.csv  – 2 097 152 bytes (2 MiB)
RUN dd if=/dev/zero of=/home/user/workshop/data/raw/big_dataset.csv bs=1024 count=2048

# raw/medium_dataset.csv – 524 288 bytes (512 KiB)
RUN dd if=/dev/zero of=/home/user/workshop/data/raw/medium_dataset.csv bs=1024 count=512

# processed/small_clean.csv – 10 240 bytes (10 KiB)
RUN dd if=/dev/zero of=/home/user/workshop/data/processed/small_clean.csv bs=1024 count=10

# extra/tiny.txt – 512 bytes
RUN dd if=/dev/zero of=/home/user/workshop/data/extra/tiny.txt bs=512 count=1

# Ensure the student (non-root container user) can freely manipulate everything
RUN chmod -R 0777 /home/user/workshop && \
    chmod 755 /home/user