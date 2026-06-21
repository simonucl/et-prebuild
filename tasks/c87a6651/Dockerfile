# syntax=docker/dockerfile:1
# Converted from Apptainer: using ubuntu:22.04 as base
FROM ubuntu:22.04

# System packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip

# Python tooling
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare required directory structure and source log file
RUN mkdir -p /home/user/api_test/logs

RUN cat > /home/user/api_test/logs/api_integration.log <<'EOF'
2024-09-10 10:15:21,345 INFO  [AuthService] - Authentication succeeded for user id 42
2024-09-10 10:15:22,103 WARN  [PaymentService] - Payment took longer than expected (842ms)
2024-09-10 10:15:23,511 ERROR [PaymentService] - Payment gateway timeout after 30000ms
2024-09-10 10:15:24,186 INFO  [NotificationService] - Email sent to user id 42
2024-09-10 10:15:25,902 ERROR [ShipmentService] - Invalid shipping address provided
2024-09-10 10:15:26,778 DEBUG [InventoryService] - Stock level for SKU-12345 is 98
2024-09-10 10:15:27,664 FATAL [InventoryService] - Database unreachable
2024-09-10 10:15:28,350 INFO  [AuthService] - Logout completed for user id 42
2024-09-10 10:15:29,021 ERROR [PaymentService] - Currency mismatch: expected USD got EUR
EOF

# Ensure readability for non-root users
RUN chmod -R a+r /home/user/api_test/logs

# Commands from %environment
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Container with initial state for API log extraction exercise."