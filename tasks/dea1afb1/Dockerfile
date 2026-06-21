FROM ubuntu:22.04

# Labels
LABEL Task="PostgreSQL slow-query filtering challenge"
LABEL Maintainer="Apptainer Task Preparer"

# Help information as comments
# This container is pre-provisioned for the "slow-query report" task.
#
# It includes:
#   • /home/user/slow_queries.csv  – the input data the student must process
#   • Python 3, pytest, csvkit, and jq – useful tools for the solution and testing
#
# The student must work entirely inside /home/user (already writeable to non-root users).

# Basic tools
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip jq && \
    pip3 install --no-cache-dir pytest csvkit

# Create working directory
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Create the slow-query CSV with the exact, specification-compliant content
RUN cat > /home/user/slow_queries.csv <<'EOF'
query_id,db,username,duration_ms,sql_text
1,inventory,alice,350,SELECT * FROM products;
2,inventory,bob,1200,UPDATE products SET price = price*1.1 WHERE category='gadgets';
3,hr,carol,900,SELECT * FROM employees WHERE salary > 70000;
4,sales,dave,2400,DELETE FROM orders WHERE order_date < '2022-01-01';
5,analytics,erin,1500,SELECT COUNT(*) FROM page_views WHERE view_date = CURRENT_DATE;
EOF

# Ensure the CSV is readable/writeable by any user
RUN chmod 0666 /home/user/slow_queries.csv

# Environment variables
ENV PATH="$PATH:/usr/local/bin"
ENV HOME=/home/user

WORKDIR /home/user