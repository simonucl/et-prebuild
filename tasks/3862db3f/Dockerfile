FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the unprivileged user
RUN useradd -m -u 1000 -s /bin/bash user

# Prepare input directory
RUN mkdir -p /home/user/vuln_scan/input

# Create banners.txt
RUN cat >/home/user/vuln_scan/input/banners.txt <<'EOF'
80/tcp open  http  Apache httpd 2.2.15 (CentOS)
22/tcp open  ssh   OpenSSH 6.0p1 Debian 4+deb7u2 (protocol 2.0)
443/tcp open  ssl/openssl  OpenSSL 1.0.1e
21/tcp open  ftp   vsftpd 2.3.4
EOF

# Set permissions
RUN chown -R user:user /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/vuln_scan && \
    chmod 755 /home/user/vuln_scan/input && \
    chmod 644 /home/user/vuln_scan/input/banners.txt

# Environment settings
ENV PATH=/usr/local/bin:/usr/bin:/bin