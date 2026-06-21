FROM ubuntu:22.04

# Install Python + pip and other dependencies
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN pip3 install --no-cache-dir pytest

# Prepare the initial filesystem state expected by the exercise
# 1. Ensure /home/user exists and is writable by the unprivileged user
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# 2. Create the backups directory and the empty image file
RUN mkdir -p /home/user/backups && \
    chmod 0755 /home/user/backups && \
    touch /home/user/backups/weekly_backup.img && \
    chmod 0644 /home/user/backups/weekly_backup.img

# 3. Intentionally DO NOT create /home/user/logs so tests can verify
#    its absence before the agent performs the task.

# Set working directory
WORKDIR /home/user

# Container for the weekly_backup verification task.
# Run your commands inside an interactive shell:
#   docker exec -it <container> /bin/bash
CMD ["/bin/bash"]