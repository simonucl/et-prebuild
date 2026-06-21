FROM ubuntu:22.04

# Install Python tooling
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/project/logs/raw

# Populate fixture log file
RUN cat > /home/user/project/logs/raw/web_access_2023-11-05.log << 'EOF'
2023-11-05T08:12:01Z 10.0.0.5 GET /api/v1/order 404 NotFound
2023-11-05T08:15:34Z 203.0.113.45 GET /api/v1/order 200 OK
2023-11-05T09:02:17Z 198.51.100.23 POST /api/v1/order 500 InternalServerError
2023-11-05T09:15:42Z 10.10.10.10 GET /api/v1/order 500 InternalServerError
2023-11-05T09:20:03Z 203.0.113.45 GET /health 200 OK
2023-11-05T10:05:55Z 198.51.100.23 GET /api/v1/order 404 NotFound
2023-11-05T10:05:55Z 198.51.100.23 GET /api/v1/order 404 NotFound
2023-11-05T11:30:44Z 192.0.2.10 GET /api/v1/order 502 BadGateway
2023-11-05T11:45:00Z 172.16.0.8 GET /api/v1/order 403 Forbidden
2023-11-05T12:00:12Z 203.0.113.45 GET /reports 404 NotFound
2023-11-05T12:05:12Z 203.0.113.45 GET /api/v1/order 403 Forbidden
2023-11-05T12:30:00Z 203.0.113.46 GET /api/v1/order 400 BadRequest
2023-11-05T12:30:00Z 10.0.0.16 GET /api/v1/order 400 BadRequest
2023-11-05T12:45:00Z 198.18.0.1 GET /api/v1/order 200 OK
2023-11-05T13:00:00Z 203.0.113.47 POST /api/v1/order 201 Created
2023-11-05T13:30:00Z 203.0.113.45 GET /api/v1/order 503 ServiceUnavailable
EOF

# Permissions
RUN chmod -R a+rwx /home/user

# Environment setup
ENV PATH="$PATH:/home/user/.local/bin"

# Help text
# Author: task-preparation-bot
# Description: Environment for web-access log cleaning exercise – raw log pre-loaded, pytest installed.

# Default run command
CMD ["/bin/bash"]