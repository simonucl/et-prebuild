FROM ubuntu:22.04

# Install Python, pip, and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create /home/user and prepare initial filesystem state
RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/scan_results

RUN cat > /home/user/scan_results/nmap_scan.log <<'EOF'
192.168.1.10:22/tcp Open VULNERABLE-OpenSSH CVE-2020-1234
192.168.1.12:80/tcp Closed
192.168.1.15:445/tcp Open VULNERABLE-SMBGhost CVE-2020-0796
10.0.0.5:3389/tcp Open Secure
172.16.0.9:22/tcp Open VULNERABLE-OpenSSH CVE-2021-28041
EOF

RUN chmod 0755 /home/user/scan_results && \
    chmod 0644 /home/user/scan_results/nmap_scan.log

# Environment settings from %environment
ENV HOME=/home/user

# Ensure directory permissions as in %environment
RUN chmod 755 /home/user

# Labels
LABEL Author="PenTest Training Container"
LABEL Description="Container for network-scan text-processing exercise"

# Run script equivalent
CMD echo "This container is for the vulnerable-host extraction exercise." && \
    echo "Enter the shell and follow the instructions in the assignment."