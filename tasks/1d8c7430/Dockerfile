FROM ubuntu:22.04

# Author: AI Assistant
# Description: Container for log-filtering task; includes raw log and pytest for grading.

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user || true

RUN mkdir -p /home/user/release/logs

RUN cat > /home/user/release/logs/deploy-2023-10-01.log <<'EOF'
2023-10-01T02:15:43Z [INFO] [user-service] Deployed successfully
2023-10-01T02:17:01Z [ERROR] [payment-service] NullPointer exception at PaymentProcessor.java:87
2023-10-01T02:18:22Z [WARN] [inventory-service] Slow response detected
2023-10-01T02:19:55Z [ERROR] [payment-service] Timeout while contacting bank API
2023-10-01T02:20:01Z [INFO] [payment-service] Health check passed
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/release && \
    chmod 755 /home/user/release/logs && \
    chmod 644 /home/user/release/logs/deploy-2023-10-01.log

LABEL Author="AI Assistant" \
      Description="Container for log-filtering task: includes raw log and pytest for grading."