FROM ubuntu:22.04

# Help text
# This container provides the initial environment for the security log-analysis
# task. The HTTP access log is pre-seeded in /home/user/network/access.log, and
# pytest is available for the grading harness.

LABEL Author="Automated build for security log-analysis exercise"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        dnsutils \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/network && \
    chmod 0755 /home/user/network

RUN cat > /home/user/network/access.log <<'EOF'
10.0.0.15 - - [12/Dec/2023:10:15:21 +0000] "GET http://localhost/index.html HTTP/1.1" 200 512
10.0.0.15 - - [12/Dec/2023:10:15:22 +0000] "GET http://example.com/assets/logo.png HTTP/1.1" 200 1024
10.0.0.15 - - [12/Dec/2023:10:15:25 +0000] "GET http://nonexistent.domain.tld/register HTTP/1.1" 404 123
EOF

RUN chmod 0644 /home/user/network/access.log && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    chmod 755 /home/user

ENV PATH="$PATH:/home/user/.local/bin"