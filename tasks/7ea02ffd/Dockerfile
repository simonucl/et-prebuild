FROM ubuntu:22.04

# Labels
LABEL Author="example"
LABEL Description="Environment for SQL refactor task with pytest pre-installed"

# Install Python tooling and pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure
RUN mkdir -p /home/user/query_scripts

# Create get_users.sql
RUN cat > /home/user/query_scripts/get_users.sql << 'EOF'
SELECT * FROM users WHERE active = 1;
-- some comment
EOF

# Create get_orders.sql
RUN cat > /home/user/query_scripts/get_orders.sql << 'EOF'
SELECT id, total FROM orders;
EOF

# Create update_users.sql
RUN cat > /home/user/query_scripts/update_users.sql << 'EOF'
UPDATE users SET active = 0 WHERE last_login < '2023-01-01';
EOF

# Create archive_customers.sql
RUN cat > /home/user/query_scripts/archive_customers.sql << 'EOF'
SELECT * FROM customers WHERE archived = 0;
EOF

# Create delete_tmp.sql
RUN cat > /home/user/query_scripts/delete_tmp.sql << 'EOF'
SELECT * FROM tmp_data;
EOF

# Set permissions: directory 0755, files 0644
RUN chmod 0755 /home/user/query_scripts && \
    find /home/user/query_scripts -type f -name "*.sql" -exec chmod 0644 {} + && \
    rm -f /home/user/query_scripts/refactor.log

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Help information (as comment)
# This Docker image provides the starting environment for the SQL
# refactoring assignment. The directory /home/user/query_scripts contains
# the legacy .sql files in their pristine state, and pytest is available
# for the automated grader.