FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state
RUN mkdir -p /home/user/security_scan && \
    chmod 755 /home/user && \
    chmod 755 /home/user/security_scan

RUN cat > /home/user/security_scan/scan_results.log <<'EOF'
/var/www/html/index.php -rw-r--r-- root
/etc/passwd -rw-r--r-- root
/tmp/tempfile.sh -rwxrwxrwx user
/home/user/public_notes.txt -rw-rw-r-- user
/var/log/app.log -rw-r----- syslog
/home/user/scripts/run.sh -rwxr-xr-x user
/opt/software/config.cfg -rw-rw-rw- user
EOF

RUN chmod 644 /home/user/security_scan/scan_results.log

CMD echo "Container for security-scan assignment." && echo "Verify the initial state with: pytest /path/to/tests"