FROM ubuntu:22.04

# Author YourName
# Description "Initial state for API key rotation task – Ubuntu 22.04 with pytest"
# This container sets up the initial environment for the API key rotation task.
# It provides:
#   • /home/user/credential_store/old_credentials.csv with the exact required data
#   • pytest installed for the automated checker

ENV HOME=/home/user

RUN set -e && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/credential_store && \
    chmod 755 /home/user && \
    chmod 755 /home/user/credential_store

RUN cat > /home/user/credential_store/old_credentials.csv <<'EOF'
service,username,old_api_key,new_api_key
auth-service,svc-auth,x8fe21ef,NEW-API-KEY-001
payment-gateway,svc-pay,98ab442b,NEW-API-KEY-002
analytics-engine,svc-ana,44cc9911,NEW-API-KEY-003
EOF

RUN chmod 644 /home/user/credential_store/old_credentials.csv

LABEL Author="YourName"
LABEL Description="Initial state for API key rotation task – Ubuntu 22.04 with pytest"