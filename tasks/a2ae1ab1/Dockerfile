FROM ubuntu:22.04

# Labels
LABEL Author="integration-task-prep"

# Install Python, pip, and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create /home/user and the logs directory
RUN mkdir -p /home/user/logs && \
    chmod 777 /home/user && \
    chmod 777 /home/user/logs

# Populate the consolidated log file
RUN cat > /home/user/logs/api_integration.log << 'EOF'
2023-09-15T08:01:22Z GET /customers 200
2023-09-15T08:01:23Z POST /orders 201
2023-09-15T08:01:25Z GET /customers/42 404
2023-09-15T08:01:27Z PATCH /customers/42 409
2023-09-15T08:01:30Z GET /inventory 200
2023-09-15T08:01:35Z GET /orders/310 500
2023-09-15T08:01:36Z POST /payments 502
2023-09-15T08:01:40Z GET /health 200
2023-09-15T08:01:45Z DELETE /customers/42 204
2023-09-15T08:01:50Z GET /customers/99 404
2023-09-15T08:01:55Z POST /orders 503
2023-09-15T08:01:59Z GET /analytics 401
EOF

# Ensure the log file is readable and writable by any user
RUN chmod 666 /home/user/logs/api_integration.log

# Set permissions on /home/user
RUN chmod 755 /home/user

# Set working directory
WORKDIR /home/user

# Help information (as comments):
# Container prepared for the API integration log-processing task.
# Initial log located at /home/user/logs/api_integration.log.
# Pytest pre-installed for automated assessment.