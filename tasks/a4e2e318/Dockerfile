FROM ubuntu:22.04

# Environment variables from %environment
ENV PATH="$PATH:/usr/local/bin"
ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        dnsutils && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/logs && \
    chmod 0777 /home/user/logs

RUN cat > /home/user/logs/local_access.log <<'EOF'
127.0.0.1 - - [10/Sep/2023:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 1024
127.0.0.1 - - [10/Sep/2023:12:00:05 +0000] "POST /login HTTP/1.1" 302 512
127.0.0.1 - - [10/Sep/2023:12:00:10 +0000] "GET /dashboard HTTP/1.1" 200 2048
EOF

RUN chmod 0644 /home/user/logs/local_access.log && \
    rm -f /home/user/logs/local_ip_hostname_mapping.csv && \
    chmod 755 /home/user

CMD ["/bin/bash"]