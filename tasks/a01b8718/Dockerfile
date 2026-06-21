FROM ubuntu:22.04

# Base tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/app/logs

# 2023-08-10 log
RUN cat <<'EOF' > /home/user/app/logs/app-2023-08-10.log
2023-08-10 08:53:02,018 - api-service - INFO  - I200 Application started
2023-08-10 09:01:44,776 - api-service - WARN  - W301 Slow response 1200ms
2023-08-10 09:42:11,667 - scheduler   - INFO  - I210 Nightly build finished
EOF

# 2023-08-11 log
RUN cat <<'EOF' > /home/user/app/logs/app-2023-08-11.log
2023-08-11 09:15:23,456 - api-service     - INFO  - I201 User login succeeded
2023-08-11 10:02:11,102 - billing-service - ERROR - E451 Payment gateway timeout
2023-08-11 11:47:05,332 - api-service     - ERROR - E401 Unauthorized access token
2023-08-11 14:30:00,908 - scheduler       - INFO  - I215 Daily job completed in 145s
EOF

# Permissions
RUN chmod -R 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Labels
LABEL Author="auto-generated"
LABEL Description="Container providing initial state for release-manager log-summary task"