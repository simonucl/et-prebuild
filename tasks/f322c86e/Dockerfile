FROM ubuntu:22.04

# Update package lists and install Python + pytest
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the required directory hierarchy for the task
RUN mkdir -p /home/user/backup/weekly

# Ensure the weekly directory is writable by any user running the container
RUN chmod 0777 /home/user/backup/weekly

# Create the empty backup file
RUN : > /home/user/backup/weekly/full_backup.tar.gz && \
    chmod 0644 /home/user/backup/weekly/full_backup.tar.gz

# Set permissions on home directory
RUN chmod 755 /home/user

# Add the default user-base install location for pip to PATH (if used)
ENV PATH="${PATH}:${HOME}/.local/bin"