FROM ubuntu:22.04

# Install Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd --create-home --shell /bin/bash user; \
    fi

# Create filesystem state
RUN mkdir -p /home/user/project/logs

RUN cat > /home/user/project/logs/access.log << 'EOF'
10.0.0.1 - - [10/Oct/2022:13:55:00 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.2 - - [10/Oct/2022:13:55:05 +0000] "GET /about.html HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
10.0.0.3 - - [10/Oct/2022:13:55:10 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.4 - - [10/Oct/2022:13:55:15 +0000] "GET /contact.html HTTP/1.1" 404 512 "-" "Mozilla/5.0"
10.0.0.5 - - [10/Oct/2022:13:55:20 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.6 - - [10/Oct/2022:13:55:25 +0000] "GET /products.html HTTP/1.1" 301 256 "-" "Mozilla/5.0"
10.0.0.7 - - [10/Oct/2022:13:55:30 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.8 - - [10/Oct/2022:13:55:35 +0000] "GET /favicon.ico HTTP/1.1" 404 128 "-" "Mozilla/5.0"
10.0.0.1 - - [10/Oct/2022:13:55:40 +0000] "GET /products.html HTTP/1.1" 301 256 "-" "Mozilla/5.0"
10.0.0.2 - - [10/Oct/2022:13:55:45 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.3 - - [10/Oct/2022:13:55:50 +0000] "GET /contact.html HTTP/1.1" 404 512 "-" "Mozilla/5.0"
10.0.0.4 - - [10/Oct/2022:13:55:55 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.5 - - [10/Oct/2022:13:56:00 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.6 - - [10/Oct/2022:13:56:05 +0000] "GET /blog.html HTTP/1.1" 200 1536 "-" "Mozilla/5.0"
10.0.0.7 - - [10/Oct/2022:13:56:10 +0000] "GET /about.html HTTP/1.1" 200 2048 "-" "Mozilla/5.0"
10.0.0.8 - - [10/Oct/2022:13:56:15 +0000] "GET /favicon.ico HTTP/1.1" 404 128 "-" "Mozilla/5.0"
10.0.0.1 - - [10/Oct/2022:13:56:20 +0000] "GET /index.html HTTP/1.1" 500 0 "-" "Mozilla/5.0"
10.0.0.2 - - [10/Oct/2022:13:56:25 +0000] "GET /index.html HTTP/1.1" 500 0 "-" "Mozilla/5.0"
10.0.0.3 - - [10/Oct/2022:13:56:30 +0000] "GET /contact.html HTTP/1.1" 404 512 "-" "Mozilla/5.0"
10.0.0.4 - - [10/Oct/2022:13:56:35 +0000] "GET /products.html HTTP/1.1" 301 256 "-" "Mozilla/5.0"
10.0.0.5 - - [10/Oct/2022:13:56:40 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
10.0.0.6 - - [10/Oct/2022:13:56:45 +0000] "GET /products.html HTTP/1.1" 301 256 "-" "Mozilla/5.0"
10.0.0.7 - - [10/Oct/2022:13:56:50 +0000] "GET /blog.html HTTP/1.1" 200 1536 "-" "Mozilla/5.0"
10.0.0.8 - - [10/Oct/2022:13:56:55 +0000] "GET /favicon.ico HTTP/1.1" 404 128 "-" "Mozilla/5.0"
10.0.0.1 - - [10/Oct/2022:13:57:00 +0000] "GET /index.html HTTP/1.1" 200 1024 "-" "Mozilla/5.0"
EOF

# Correct ownership
RUN chown -R user:user /home/user && chmod 755 /home/user

# Environment variables
ENV LANG=C
ENV LC_ALL=C

LABEL Author="Apptainer automation bot – initial state for Apache log task"

CMD ["/bin/bash"]