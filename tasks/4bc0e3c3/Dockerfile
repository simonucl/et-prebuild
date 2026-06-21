FROM ubuntu:22.04

# Help text
# This container provides the initial state required for the audit-trail
# exercise. It already contains three micro-service log files under
# /home/user/services/... as well as pytest for automated grading.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN base_dir="/home/user/services" && \
    mkdir -p "${base_dir}/auth/logs" \
             "${base_dir}/orders/logs" \
             "${base_dir}/payments/logs"

RUN base_dir="/home/user/services" && \
    cat > "${base_dir}/auth/logs/service.log" << 'EOF'
2023-10-30T23:59:59Z INFO Startup complete
2023-10-31T00:00:02Z ERROR Token validation failed for user id 42
2023-10-31T06:30:11Z WARN Token near expiry for user id 7
2023-10-31T22:15:45Z ERROR Unauthorized access attempt detected
EOF

RUN base_dir="/home/user/services" && \
    cat > "${base_dir}/orders/logs/service.log" << 'EOF'
2023-10-31T01:15:22Z INFO Order service started
2023-10-31T02:47:05Z ERROR Order ID 1001 failed validation
2023-10-31T14:22:33Z ERROR Payment gateway timeout for order 2033
EOF

RUN base_dir="/home/user/services" && \
    cat > "${base_dir}/payments/logs/service.log" << 'EOF'
2023-10-31T03:10:00Z ERROR Credit card declined transaction 5005
2023-10-31T12:00:00Z INFO Daily settlement completed
2023-10-31T20:59:59Z ERROR Fraud detection triggered for transaction 6006
EOF

RUN chmod -R 755 /home/user && \
    find /home/user/services -type f -name "service.log" -exec chmod 644 {} \;

# Labels (informational only)
LABEL author="AI Assistant"
LABEL description="Container for ERROR-only audit trail task with pre-populated service logs and pytest installed."