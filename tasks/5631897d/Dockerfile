# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer Task Generator" \
      Description="Container with initial state for IP frequency report assignment"

# Install Python, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare the initial filesystem state expected by the assignment
RUN set -e && \
    mkdir -p /home/user/audit

RUN cat > /home/user/audit/raw_login_attempts.log <<'EOF'
192.168.1.10
10.0.0.5
192.168.1.10
8.8.8.8
10.0.0.5
10.0.0.5
203.0.113.1
8.8.8.8
192.168.1.10
198.51.100.2
203.0.113.1
203.0.113.1
127.0.0.1
192.168.1.10
127.0.0.1
EOF

# Ensure the runtime (non-root) user can create the required report file
RUN chmod 0777 /home/user/audit && \
    chmod 0644 /home/user/audit/raw_login_attempts.log && \
    chmod 0755 /home/user || true

# Environment setup
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH}"