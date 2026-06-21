FROM ubuntu:22.04

# Labels
LABEL Author="web-dev-task-prep"
LABEL Description="Starter image for IP frequency report assignment (pytest pre-installed)"

# Update package index and install Python + pip
RUN set -e && \
    echo "Updating package index and installing Python + pip..." && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN echo "Installing pytest..." && \
    pip3 install --no-cache-dir pytest

# Create working directory
RUN echo "Creating working directory and populating sample access-log..." && \
    mkdir -p /home/user/log-analysis

# Create sample access log file
RUN cat > /home/user/log-analysis/sample_access.log << 'EOF'
192.168.1.10 - - [10/May/2024:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024
203.0.113.5 - - [10/May/2024:10:00:03 +0000] "POST /login HTTP/1.1" 302 512
192.168.1.10 - - [10/May/2024:10:00:04 +0000] "GET /dashboard HTTP/1.1" 200 2048
198.51.100.23 - - [10/May/2024:10:00:05 +0000] "GET /index.html HTTP/1.1" 200 1024
203.0.113.5 - - [10/May/2024:10:00:06 +0000] "GET /profile HTTP/1.1" 200 1024
192.0.2.45 - - [10/May/2024:10:00:07 +0000] "GET /index.html HTTP/1.1" 404 256
192.168.1.10 - - [10/May/2024:10:00:08 +0000] "GET /settings HTTP/1.1" 200 1024
198.51.100.23 - - [10/May/2024:10:00:09 +0000] "GET /contact HTTP/1.1" 200 512
203.0.113.5 - - [10/May/2024:10:00:10 +0000] "GET /dashboard HTTP/1.1" 200 1024
203.0.113.5 - - [10/May/2024:10:00:11 +0000] "GET /logout HTTP/1.1" 200 256
192.0.2.45 - - [10/May/2024:10:00:12 +0000] "POST /login HTTP/1.1" 302 512
192.0.2.45 - - [10/May/2024:10:00:13 +0000] "GET /home HTTP/1.1" 200 1024
192.168.1.10 - - [10/May/2024:10:00:14 +0000] "GET /logout HTTP/1.1" 200 256
198.51.100.23 - - [10/May/2024:10:00:15 +0000] "GET /settings HTTP/1.1" 200 1024
192.0.2.45 - - [10/May/2024:10:00:16 +0000] "GET /contact HTTP/1.1" 200 512
EOF

# Set appropriate permissions
RUN chmod 0644 /home/user/log-analysis/sample_access.log && \
    chmod 0777 /home/user/log-analysis && \
    chmod 0777 /home/user && \
    echo "Container setup complete."

WORKDIR /home/user

CMD ["/bin/bash"]