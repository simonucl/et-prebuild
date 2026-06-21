FROM ubuntu:22.04

# Labels
LABEL Author="task-setup"
LABEL Description="Docker image for the Nmap-to-CSV parsing exercise."

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Store the canonical Nmap sample output inside the image
RUN mkdir -p /opt/task_data

RUN cat > /opt/task_data/sample_nmap_output.txt << 'EOF'
Starting Nmap 7.93 ( https://nmap.org ) at 2023-06-15 12:34 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000093s latency).
Not shown: 995 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
25/tcp   filtered smtp
80/tcp   open  http
111/tcp  open  rpcbind
139/tcp  closed netbios-ssn
443/tcp  open  https
3306/tcp open  mysql

Nmap done: 1 IP address (1 host up) scanned in 0.19 seconds
EOF

RUN chmod 644 /opt/task_data/sample_nmap_output.txt

# Create user and home directory
RUN useradd -m -s /bin/bash -d /home/user user

# Create the setup script for container startup
RUN mkdir -p /usr/local/bin

RUN cat > /usr/local/bin/setup_task.sh << 'EENV'
#!/bin/sh
# Populate /home/user with the prerequisite directories and files
# if they are missing.
set -e

HOME_BASE="/home/user"
NT_DIR="${HOME_BASE}/network_targets"
SR_DIR="${HOME_BASE}/scan_reports"
SAMPLE_FILE="${NT_DIR}/sample_nmap_output.txt"
IMAGE_SAMPLE="/opt/task_data/sample_nmap_output.txt"

# Ensure network_targets directory and sample file
if [ ! -f "${SAMPLE_FILE}" ]; then
    mkdir -p "${NT_DIR}"
    cp "${IMAGE_SAMPLE}" "${SAMPLE_FILE}"
    chmod 644 "${SAMPLE_FILE}"
fi
chmod 755 "${NT_DIR}" 2>/dev/null || true

# Ensure scan_reports directory (empty to begin with)
if [ ! -d "${SR_DIR}" ]; then
    mkdir -p "${SR_DIR}"
fi
chmod 755 "${SR_DIR}" 2>/dev/null || true

# Fix ownership
chown -R user:user "${HOME_BASE}" 2>/dev/null || true
EENV

RUN chmod +x /usr/local/bin/setup_task.sh

# Set up the initial directory structure
RUN /usr/local/bin/setup_task.sh

# Set permissions on home directory
RUN chmod 755 /home/user && chown -R user:user /home/user

# Environment variables
ENV HOME=/home/user

WORKDIR /home/user
USER user