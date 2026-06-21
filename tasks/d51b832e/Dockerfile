FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create required directory structure
RUN mkdir -p /home/user/backups && \
    mkdir -p /home/user/backup_scripts && \
    chmod 755 /home/user/backups && \
    chmod 755 /home/user/backup_scripts

# Populate /home/user/backups/ with the specified files
# Each file is created with the exact byte size and permissions needed
RUN truncate -s 12345 /home/user/backups/prod_2023-09-01.sql && \
    truncate -s 23456 /home/user/backups/prod_2023-09-02.sql && \
    truncate -s 34567 /home/user/backups/prod_2023-09-03.sql && \
    truncate -s 45678 /home/user/backups/staging_2023-09-01.dump && \
    truncate -s 56789 /home/user/backups/staging_2023-09-02.dump && \
    chmod 600 /home/user/backups/prod_2023-09-01.sql && \
    chmod 660 /home/user/backups/prod_2023-09-02.sql && \
    chmod 666 /home/user/backups/prod_2023-09-03.sql && \
    chmod 644 /home/user/backups/staging_2023-09-01.dump && \
    chmod 606 /home/user/backups/staging_2023-09-02.dump

# Labels
LABEL Maintainer="task-preparation-bot"

# Help information:
# This container provides the starting filesystem state for the
# "backup security audit" task. Pytest is pre-installed so that the
# grading harness can verify the initial conditions.