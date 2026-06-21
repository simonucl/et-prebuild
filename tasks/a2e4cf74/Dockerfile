FROM ubuntu:22.04

# Help / labels
LABEL Author="Container Setup for Package-Version Exercise"

# Install Python and Pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Prepare filesystem state
RUN mkdir -p /home/user/pkg_scan && \
    chmod 0777 /home/user/pkg_scan

# Create installed packages baseline file
RUN cat > /home/user/pkg_scan/installed_packages.txt <<'EOF'
ii  openssl  1.1.1f-1ubuntu2  amd64  Secure Sockets Layer toolkit – cryptographic utility
ii  curl     7.68.0-1ubuntu2  amd64  command line tool for transferring data with URL syntax
ii  nmap     7.80+dfsg1-2     amd64  The Network Mapper
ii  lynx     2.9.0-1          amd64  Text-mode WWW Browser
ii  nano     4.8-1ubuntu1     amd64  small, friendly text editor inspired by Pico
EOF

RUN chmod 0644 /home/user/pkg_scan/installed_packages.txt

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Permissions from %environment
RUN chmod 755 /home/user