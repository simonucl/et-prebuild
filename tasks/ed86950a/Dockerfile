FROM ubuntu:22.04

# Help text
# This container provides the initial filesystem state required for the
# “Customer Snapshot Encryption & Audit-Log” exercise.
# - Plaintext CSV: /home/user/etl/input/customer_snapshot.csv
# - Encrypted output directory: /home/user/etl/encrypted
# Tools installed: gpg, sha256sum, pytest.

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        gnupg \
        coreutils \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/etl/input && \
    mkdir -p /home/user/etl/encrypted

RUN cat <<'EOF' > /home/user/etl/input/customer_snapshot.csv
customer_id,name,signup_date
101,Alice,2023-01-02
102,Bob,2023-01-10
103,Charlie,2023-01-15
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/etl && \
    chmod 755 /home/user/etl/input && \
    chmod 777 /home/user/etl/encrypted