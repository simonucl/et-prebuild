FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Setup"

# Environment variables
ENV PATH="/usr/bin:$PATH"

# Update APT index and install Python tooling
RUN set -e && \
    echo "Updating APT index and installing Python tooling..." && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating initial directory structure and log file..." && \
    mkdir -p /home/user/logs

# Create the log file with the exact required contents (trailing newline included)
RUN cat > /home/user/logs/user_mgmt.log << 'LOGEOF'
[2023-09-30 23:59:59] INFO system: ADD user=alice id=1001
[2023-10-01 00:00:01] INFO system: ADD user=bob id=1002
[2023-10-05 12:34:56] INFO system: DEL user=charlie id=1003
[2023-10-15 08:00:00] INFO system: ADD user=david id=1004
[2023-10-20 14:15:30] INFO system: DEL user=alice id=1001
[2023-10-31 23:59:59] INFO system: ADD user=erin id=1005
[2023-11-01 00:00:01] INFO system: ADD user=frank id=1006
LOGEOF

# Ensure permissions allow the unprivileged host user to work in /home/user
RUN chmod 0777 /home/user && \
    chmod 0755 /home/user/logs && \
    chmod 0644 /home/user/logs/user_mgmt.log

# Clean up APT caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/user

# Default command
CMD echo "Container for the October 2023 user-account audit task." && echo "Use this environment to solve the exercise."