FROM ubuntu:22.04

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/db_logs && \
    chmod 755 /home/user/db_logs

RUN cat <<'EOF' >/home/user/db_logs/slow_query.log
# Time: 2023-10-11T10:15:23
# User@Host: root[root] @ localhost []
# Query_time: 3.125 Lock_time: 0.000 Rows_sent: 12 Rows_examined: 100
SET timestamp=1697024123;
SELECT * FROM users WHERE id = 42;
# Time: 2023-10-11T10:16:00
# User@Host: app[app] @ 192.168.1.10 []
# Query_time: 0.256 Lock_time: 0.001 Rows_sent: 1 Rows_examined: 5
SET timestamp=1697024160;
SELECT name FROM products WHERE price > 1000;
# Time: 2023-10-11T10:17:35
# User@Host: analytics[anl] @ 192.168.1.20 []
# Query_time: 7.890 Lock_time: 0.002 Rows_sent: 25000 Rows_examined: 500000
SET timestamp=1697024255;
SELECT email, created_at FROM audit_logs WHERE created_at < '2023-01-01';
# Time: 2023-10-11T10:18:12
# User@Host: root[root] @ localhost []
# Query_time: 1.050 Lock_time: 0.000 Rows_sent: 0 Rows_examined: 0
SET timestamp=1697024292;
DELETE FROM sessions WHERE last_activity < NOW() - INTERVAL 30 DAY;
# Time: 2023-10-11T10:20:44
# User@Host: api[api] @ 192.168.1.30 []
# Query_time: 12.500 Lock_time: 0.010 Rows_sent: 5 Rows_examined: 1500000
SET timestamp=1697024444;
UPDATE orders SET status='FAILED' WHERE payment_state='error';
# Time: 2023-10-11T10:22:05
# User@Host: app[app] @ 192.168.1.10 []
# Query_time: 0.600 Lock_time: 0.001 Rows_sent: 1 Rows_examined: 10
SET timestamp=1697024525;
SELECT name FROM customers WHERE customer_id = 123;
EOF

RUN chmod 644 /home/user/db_logs/slow_query.log

RUN rm -f /home/user/db_logs/query_metrics.log /home/user/db_logs/high_latency_queries.sql