FROM ubuntu:22.04

# Labels
LABEL Author="junior-security-auditor-task"
LABEL Description="Base image with Python, pytest, and networking tools pre-installed."

# Update package lists and install required utilities
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        iproute2 \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0755 /home/user || true && \
    chown 1000:1000 /home/user || true && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

# Help information (as comments):
# This container image supplies Python 3, pytest, and standard networking
# tools (ip, ss) required for the "network exposure snapshot" task.
# It intentionally does NOT create /home/user/audit nor the target log file
# so that students can generate them during their exercise.