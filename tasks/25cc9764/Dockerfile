FROM ubuntu:22.04

# Install Python, pip and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial workspace expected by the exercise & tests
RUN mkdir -p /home/user/data

# Create the reference authentication log with exact byte-for-byte
# content (Unix LF endings, single trailing LF).
RUN cat > /home/user/data/auth.log <<'EOF'
2023-05-14T08:14:22Z|admin|192.168.1.45|FAILED_LOGIN
2023-05-14T08:14:26Z|john|192.168.1.23|SUCCESSFUL_LOGIN
2023-05-14T08:15:02Z|root|10.0.0.15|FAILED_LOGIN
2023-05-14T08:15:45Z|mary|192.168.1.23|SESSION_CLOSED
2023-05-14T08:16:03Z|test|172.16.0.8|FAILED_LOGIN
2023-05-14T08:16:48Z|john|192.168.1.23|SUDO_SESSION_OPENED
EOF

# Make sure future (non-root) users can work under /home/user
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PYTHONUSERBASE=/home/user/.local

WORKDIR /home/user

# Default action: drop into an interactive shell
CMD ["/bin/bash"]