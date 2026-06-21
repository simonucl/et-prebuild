FROM ubuntu:22.04

# Install Python 3, pip and pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure and log files expected by tests
# Ensure /home/user exists
RUN mkdir -p /home/user

# Distributed logs directory
RUN mkdir -p /home/user/distributed-logs

# 1. frontend.log
RUN cat > /home/user/distributed-logs/frontend.log <<'EOF'
[2023-07-01 10:00:00] Service frontend: HealthCheck: OK
[2023-07-01 10:05:00] Service frontend: HealthCheck: OK
[2023-07-01 10:10:00] Service frontend: HealthCheck: FAILED
[2023-07-01 10:15:00] Service frontend: HealthCheck: OK
EOF

# 2. backend.log
RUN cat > /home/user/distributed-logs/backend.log <<'EOF'
[2023-07-01 10:00:00] Service backend: HealthCheck: OK
[2023-07-01 10:05:00] Service backend: HealthCheck: FAILED
[2023-07-01 10:10:00] Service backend: HealthCheck: FAILED
EOF

# 3. auth.log
RUN cat > /home/user/distributed-logs/auth.log <<'EOF'
[2023-07-01 10:00:00] Service auth: HealthCheck: OK
[2023-07-01 10:05:00] Service auth: HealthCheck: OK
EOF

# 4. payments.log
RUN cat > /home/user/distributed-logs/payments.log <<'EOF'
[2023-07-01 10:00:00] Service payments: HealthCheck: FAILED
[2023-07-01 10:05:00] Service payments: HealthCheck: OK
EOF

# 5. cache.log
RUN cat > /home/user/distributed-logs/cache.log <<'EOF'
[2023-07-01 10:00:00] Service cache: HealthCheck: OK
[2023-07-01 10:05:00] Service cache: HealthCheck: OK
EOF

# Ensure permissions allow non-root users to read/write where needed
RUN chmod -R a+rwX /home/user

# Set environment variables
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /home/user

CMD ["echo", "This container is prepared for the distributed logs task. Run your solution script or tests as needed."]