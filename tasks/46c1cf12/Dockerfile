FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare directory structure
RUN mkdir -p /home/user/data && \
    chmod 0777 /home/user

# Create CSV dataset
RUN cat >/home/user/data/transactions.csv <<'EOF'
transaction_id,account_id,amount,currency,status
T1001,AC245,250.00,USD,COMPLETED
T1002,AC367,1450.50,USD,PENDING
T1003,AC578,322.10,EUR,FAILED
T1004,AC245,78.45,USD,COMPLETED
T1005,AC367,2300.00,USD,FAILED
EOF

RUN chmod 0644 /home/user/data/transactions.csv

ENV PYTHONUNBUFFERED=1

# Maintainer compliance-container-builder