FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gzip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/db_backups

# 1. customers.sql (68 bytes, including trailing newline)
RUN cat > /home/user/db_backups/customers.sql <<'EOF'
-- Customers table backup
INSERT INTO customers VALUES (1,'Alice');
EOF

# 2. orders.sql (71 bytes)
RUN cat > /home/user/db_backups/orders.sql <<'EOF'
-- Orders table backup
INSERT INTO orders VALUES (101,1,'2023-01-01');
EOF

# 3. inventory.sql (75 bytes)
RUN cat > /home/user/db_backups/inventory.sql <<'EOF'
-- Inventory table backup
INSERT INTO inventory VALUES (1001,'Widget',50);
EOF

# Ensure the runtime (non-root) user can manipulate the backup area.
RUN chmod 0755 /home/user && \
    chmod 0777 /home/user/db_backups

CMD echo "Container for the database-backup cleanup task." && echo "Inspect /home/user/db_backups to begin."