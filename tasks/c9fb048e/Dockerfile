FROM ubuntu:22.04

# Author: ChatGPT
# Description: Environment for "optimize_slow_queries" task – initial state only.
#
# This Docker image sets up the initial filesystem state for the
# "optimize_slow_queries" exercise. It installs Python, pytest, and
# provides /home/user/db_queries.log with the required contents and
# permissions. No solution script or report file is present; those will
# be created by the learner.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN cat > /home/user/db_queries.log <<'EOF'
1,1800,SELECT id, name FROM customers WHERE vip = true;
2,3050,UPDATE products SET stock = stock - 1 WHERE id = 987;
3,150,DELETE FROM sessions WHERE last_access < NOW() - INTERVAL '30 days';
4,4990,SELECT * FROM orders WHERE status = 'PENDING';
5,2400,INSERT INTO audit_log (event) VALUES ('user_login');
EOF

RUN chmod 0644 /home/user/db_queries.log && \
    chmod 755 /home/user