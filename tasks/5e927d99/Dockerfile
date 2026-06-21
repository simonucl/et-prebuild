# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create directory structure and set permissions
RUN mkdir -p /home/user/logs && \
    chmod 0777 /home/user

# Create service-auth log
RUN cat > /home/user/logs/service-auth.log <<'EOF'
[2024-06-01 10:00:00] INFO User login successful
[2024-06-01 10:01:00] ERROR Invalid credentials
[2024-06-01 10:02:00] INFO Token issued
[2024-06-01 10:03:00] ERROR Session expired
[2024-06-01 10:04:00] ERROR Invalid credentials
EOF

# Create service-payment log
RUN cat > /home/user/logs/service-payment.log <<'EOF'
[2024-06-01 10:05:00] INFO Payment initiated
[2024-06-01 10:06:00] ERROR Card declined
[2024-06-01 10:07:00] ERROR Timeout contacting bank
[2024-06-01 10:08:00] INFO Payment retried
[2024-06-01 10:09:00] ERROR Card declined
EOF

# Create service-order log
RUN cat > /home/user/logs/service-order.log <<'EOF'
[2024-06-01 10:10:00] INFO Order placed
[2024-06-01 10:11:00] ERROR Inventory shortage
[2024-06-01 10:12:00] ERROR Inventory shortage
[2024-06-01 10:13:00] INFO Order cancelled
[2024-06-01 10:14:00] ERROR Payment pending
EOF

# Ensure world-readable log files
RUN chmod 0644 /home/user/logs/service-*.log

# Ensure /home/user has correct permissions at runtime
RUN chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1