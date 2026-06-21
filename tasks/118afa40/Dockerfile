# Container for the “checksum-verification report” exercise.
# It ships with the initial backup archives and checksum listing under
#   /home/user/backups/
# Pytest is pre-installed so the evaluation harness can run its tests.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/backups

RUN touch /home/user/backups/db_customers_full_20230710.sql.gz && \
    touch /home/user/backups/db_orders_full_20230710.sql.gz

RUN cat <<'EOF' > /home/user/backups/db_inventory_full_20230710.sql.gz
INVENTORY BACKUP
item_id,item_name,stock
1001,Widget,150
1002,Gadget,200
EOF

RUN cat <<'EOF' > /home/user/backups/expected_checksums.sha256
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  db_customers_full_20230710.sql.gz
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  db_orders_full_20230710.sql.gz
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  db_inventory_full_20230710.sql.gz
EOF

RUN chmod 755 /home/user && \
    chmod 700 /home/user/backups && \
    chmod 644 /home/user/backups/*

LABEL Author="checksum-task-preparer"