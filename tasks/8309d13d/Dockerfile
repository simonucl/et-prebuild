FROM ubuntu:22.04

# Labels
LABEL Author="payment-platform-setup"
LABEL Description="Container pre-provisioned with payment platform logs for incident-triage exercise"

# Install required software (Python, pip, pytest, gzip just in case)
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        gzip && \
    pip3 install --no-cache-dir pytest

# Create unprivileged user `user`
RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user || true

# Create log directory structure
RUN mkdir -p /home/user/logs/archive

# sys01 log
RUN cat > /home/user/logs/sys01-2023-10-15.log <<'EOF'
2023-10-15T13:59:59Z [service:billing] ERROR E1024 Card declined for user 000
2023-10-15T14:05:12Z [service:billing] ERROR E1024 Card declined for user 123
2023-10-15T14:07:30Z [service:billing] ERROR E1024 Card declined for user 456
2023-10-15T14:15:50Z [service:checkout] ERROR E2048 Inventory mismatch for product 789
2023-10-15T15:10:00Z [service:checkout] ERROR E2048 Inventory mismatch for product 654
2023-10-15T15:20:17Z [service:search]  ERROR E3001 Search backend timeout
2023-10-15T16:10:00Z [service:billing] ERROR E1024 Card declined for user 321
EOF

# sys02 log
RUN cat > /home/user/logs/sys02-2023-10-15.log <<'EOF'
2023-10-15T14:45:00Z [service:billing] ERROR E1024 Card declined for user 789
2023-10-15T14:50:22Z [service:user]    ERROR E5000 Unable to fetch profile
2023-10-15T15:05:36Z [service:user]    ERROR E5000 Unable to fetch profile
2023-10-15T15:22:01Z [service:search]  ERROR E3001 Search backend timeout
2023-10-15T15:45:59Z [service:checkout] ERROR E2048 Inventory mismatch for product 321
EOF

# sys03 compressed log
RUN cat > /tmp/sys03-2023-10-15.log <<'EOF'
2023-10-15T14:30:00Z [service:billing] ERROR E1024 Card declined for user 999
2023-10-15T15:12:12Z [service:search]  ERROR E3001 Search backend timeout
EOF

RUN gzip -c /tmp/sys03-2023-10-15.log > /home/user/logs/archive/sys03-2023-10-15.log.gz && \
    rm /tmp/sys03-2023-10-15.log

# Ensure ownership for the unprivileged user
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"