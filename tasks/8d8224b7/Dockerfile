FROM ubuntu:22.04

# Help:
# Container prepared for the slow-query log extraction exercise.
# Includes pytest for verification and the pre-populated /home/user/db_logs/queries.log file.

LABEL Author="Apptainer build for SQL log extraction task"

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/db_logs && \
    chmod 755 /home/user/db_logs

RUN cat > /home/user/db_logs/queries.log <<'EOF'
2024-06-01 09:12:11 | SELECT * FROM users; | 234ms
2024-06-01 09:12:12 | SELECT * FROM orders WHERE price > 100; | 1245ms
2024-06-01 09:12:13 | UPDATE users SET name='Alice' WHERE id=5; | 67ms
2024-06-01 09:12:14 | SELECT * FROM transactions WHERE status='failed'; | 5344ms
2024-06-01 09:12:15 | DELETE FROM sessions WHERE last_active < NOW() - INTERVAL '1 day'; | 908ms
2024-06-01 09:12:16 | SELECT COUNT(*) FROM users; | 321ms
2024-06-01 09:12:17 | INSERT INTO logs(message) VALUES('test'); | 45ms
2024-06-01 09:12:18 | SELECT * FROM orders WHERE status='pending'; | 1023ms
EOF

RUN chmod 644 /home/user/db_logs/queries.log