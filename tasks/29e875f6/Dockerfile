FROM ubuntu:22.04

# Help / labels
LABEL Author="Compliance Sweep Exercise Setup"

# Post section
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    mkdir -p /home/user/audit_data/subdir && \
    chmod 0755 /home/user/audit_data && \
    chmod 0755 /home/user/audit_data/subdir && \
    truncate -s 512 /home/user/audit_data/secure.txt && \
    chmod 0644 /home/user/audit_data/secure.txt && \
    truncate -s 2048 /home/user/audit_data/public.log && \
    chmod 0666 /home/user/audit_data/public.log && \
    truncate -s 256 /home/user/audit_data/notes && \
    chmod 0600 /home/user/audit_data/notes && \
    truncate -s 1024 /home/user/audit_data/subdir/expose.sh && \
    chmod 0777 /home/user/audit_data/subdir/expose.sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Commands from %environment that are actual shell commands
RUN chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1