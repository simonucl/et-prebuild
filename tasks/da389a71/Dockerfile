FROM ubuntu:22.04

# Labels
LABEL Author="incident-prep-bot"
LABEL Description="Pre-configured environment for incident-response assignment."

# Base packages + pytest
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create required directory hierarchy
RUN mkdir -p /home/user/microservices/auth && \
    mkdir -p /home/user/microservices/orders && \
    mkdir -p /home/user/microservices/payments

# Create auth/service.log
RUN cat > /home/user/microservices/auth/service.log <<'EOF'
2023-10-05T14:23:05Z INFO  correlation_id=a1b2c message="login attempt"
2023-10-05T14:24:55Z INFO  correlation_id=7e19a message="validate token start"
2023-10-05T14:26:03Z ERROR correlation_id=7e19a message="failed to validate token"
2023-10-05T14:28:00Z INFO  correlation_id=abc123 message="refresh token"
EOF

# Create orders/service.log
RUN cat > /home/user/microservices/orders/service.log <<'EOF'
2023-10-05T14:24:58Z INFO  correlation_id=7e19a message="create order start"
2023-10-05T14:26:04Z ERROR correlation_id=7e19a message="order creation failed: auth error"
2023-10-05T14:29:59Z INFO  correlation_id=d4f20 message="create order start"
2023-10-05T14:30:10Z ERROR correlation_id=d4f20 message="order creation failed: db timeout"
EOF

# Create payments/service.log
RUN cat > /home/user/microservices/payments/service.log <<'EOF'
2023-10-05T14:26:05Z ERROR correlation_id=7e19a message="payment aborted due to order failure"
2023-10-05T14:31:00Z INFO  correlation_id=d4f20 message="charge start"
2023-10-05T14:31:02Z ERROR correlation_id=d4f20 message="charge failed: upstream order error"
EOF

# Set permissions
RUN chmod -R 0755 /home/user && \
    chmod 0644 /home/user/microservices/*/service.log

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin