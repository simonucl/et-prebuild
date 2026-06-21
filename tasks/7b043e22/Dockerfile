# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tooling and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#################################################################
# Create required directory structure
#################################################################
RUN mkdir -p /home/user/microservices/logs/auth-service && \
    mkdir -p /home/user/microservices/logs/billing-service && \
    mkdir -p /home/user/microservices/logs/shipping-service && \
    mkdir -p /home/user/backups

# auth-service logs
RUN cat <<'EOF' > /home/user/microservices/logs/auth-service/auth.log
2023-10-05T10:00:01Z INFO  User login OK
EOF

RUN cat <<'EOF' > /home/user/microservices/logs/auth-service/error.log
2023-10-05T11:02:15Z ERROR Invalid token
EOF

# billing-service logs
RUN cat <<'EOF' > /home/user/microservices/logs/billing-service/billing.log
2023-10-05T09:14:33Z INFO  Invoice generated
EOF

RUN cat <<'EOF' > /home/user/microservices/logs/billing-service/error.log
2023-10-05T09:15:00Z WARN  Retry payment
EOF

# shipping-service logs
RUN cat <<'EOF' > /home/user/microservices/logs/shipping-service/shipping.log
2023-10-05T08:45:12Z INFO  Package shipped
EOF

RUN cat <<'EOF' > /home/user/microservices/logs/shipping-service/error.log
2023-10-05T08:46:20Z ERROR Address not found
EOF

# Permissions
RUN chmod -R a+rX /home/user/microservices && \
    chmod 0777 /home/user/backups && \
    chmod 755 /home/user

LABEL Author="backup-task" \
      Task="service-log-backup-initial-state"