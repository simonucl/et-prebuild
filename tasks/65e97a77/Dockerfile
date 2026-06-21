# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Update package lists and install Python + pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# ------------------------------------------------------------------
# Set up the initial file-system state for the “web-log filtering” task
# ------------------------------------------------------------------

# Create required directory hierarchy
RUN mkdir -p /home/user/projects/weblog

# Write the canonical Apache access log (exact eight lines, trailing newline)
RUN cat > /home/user/projects/weblog/access.log <<'EOF'
93.184.216.34 - - [10/Jun/2024:13:55:36 +0000] "GET /assets/logo.png HTTP/1.1" 200 5321 "https://example.com/" "Mozilla/5.0"
185.199.110.153 - - [10/Jun/2024:13:55:37 +0000] "GET /api/user?id=42 HTTP/1.1" 200 1234 "-" "curl/8.5.0"
203.0.113.7 - - [10/Jun/2024:13:55:37 +0000] "GET /assets/banner.JPG HTTP/1.1" 200 23122 "https://example.com/" "Mozilla/5.0"
203.0.113.7 - - [10/Jun/2024:13:55:38 +0000] "GET /assets/banner.JPG HTTP/1.1" 304 0 "https://example.com/" "Mozilla/5.0"
192.0.2.44 - - [10/Jun/2024:13:55:39 +0000] "POST /login HTTP/1.1" 302 0 "https://example.com/login" "Mozilla/5.0"
198.51.100.23 - - [10/Jun/2024:13:55:40 +0000] "GET /assets/sprite.gif HTTP/1.1" 200 998 "https://example.com/" "Mozilla/5.0"
198.51.100.23 - - [10/Jun/2024:13:55:41 +0000] "GET /assets/sprite.gif HTTP/1.1" 404 209 "https://example.com/" "Mozilla/5.0"
203.0.113.9 - - [10/Jun/2024:13:55:42 +0000] "GET /assets/bg.jpeg HTTP/1.1" 200 14231 "https://example.com/" "Mozilla/5.0"
EOF

# Permissions
RUN chmod 644 /home/user/projects/weblog/access.log && \
    chmod 777 /home/user/projects && \
    chmod 777 /home/user/projects/weblog && \
    chmod 777 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8