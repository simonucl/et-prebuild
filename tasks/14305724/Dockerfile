# Help: This container sets up the initial state for the “slow query” SQL log processing task.
# Included:
# - /home/user/db/slow_query.log (14‑line source log)
# - pytest (installed for the validation suite)
# The student/agent must create:
# - slow_query_frequency.tsv
# - slow_query_summary.log
# Both inside /home/user/db.
# Author: Apptainer slow-query task container

FROM ubuntu:22.04

ENV LANG=C
ENV LC_ALL=C

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/db

RUN cat > /home/user/db/slow_query.log <<'EOF'
SELECT * FROM orders WHERE status = 'pending';
SELECT id, name FROM customers WHERE country = 'US';
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 42;
SELECT * FROM orders WHERE status = 'pending';
SELECT * FROM orders WHERE status = 'pending';
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 42;
SELECT id, name FROM customers WHERE country = 'US';
DELETE FROM sessions WHERE last_active < NOW() - INTERVAL '30 days';
SELECT * FROM orders WHERE status = 'pending';
DELETE FROM sessions WHERE last_active < NOW() - INTERVAL '30 days';
SELECT * FROM orders WHERE status = 'pending';
SELECT id, name FROM customers WHERE country = 'US';
INSERT INTO audit_log (event, created_at) VALUES ('login', NOW());
SELECT * FROM orders WHERE status = 'pending';
EOF

RUN chmod -R a+rw /home/user/db && \
    chmod 755 /home/user