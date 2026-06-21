# This container sets up the initial state for the CSV PII-cleaning task.
# Two raw CSV files with PII live in /home/user/raw_data. Pytest is installed
# for the autograder. Create cleaned_data and scan_logs as instructed.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales && \
    locale-gen en_US.UTF-8 && \
    python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 777 /home/user && \
    mkdir -p /home/user/raw_data && \
    chmod 755 /home/user/raw_data

RUN cat > /home/user/raw_data/customers.csv <<'EOF'
id,name,email,ssn,phone,country
1,Jane Doe,jane.doe@example.com,123-45-6789,555-1234,US
2,Bob Smith,bob.smith@example.net,987-65-4321,555-2345,US
EOF

RUN cat > /home/user/raw_data/transactions.csv <<'EOF'
txn_id,card_number,cvv,amount,email,ssn
T1001,4242424242424242,123,19.99,alice@data.org,000-12-3456
T1002,4000056655665556,999,7.50,bob.smith@example.net,987-65-4321
EOF

RUN chmod 644 /home/user/raw_data/*.csv && \
    rm -rf /home/user/cleaned_data /home/user/scan_logs || true

CMD echo "CSV PII-cleaning challenge container." && \
    echo "Raw datasets are located in /home/user/raw_data." && \
    exec "$@"