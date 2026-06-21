FROM ubuntu:22.04

RUN set -e && \
    # Install Python, pip and pytest
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial filesystem state for the exercise
# ------------------------------------------------------------------
# 1. Create the backup directory
RUN mkdir -p /home/user/backup

# 2. Create the 4-byte "archive" (contents: ASCII word "test")
RUN printf "test" > /home/user/backup/old_project.tar.gz

# 3. Create the reference checksum file with TWO spaces before filename
RUN printf "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08  old_project.tar.gz\n" \
    > /home/user/backup/checksums.txt

# 4. Ensure learners can append their own log file later
RUN chmod -R a+rwX /home/user/backup

RUN chmod 755 /home/user

LABEL Author="checksum-exercise-builder"
LABEL Description="Base image for the archive checksum verification task"