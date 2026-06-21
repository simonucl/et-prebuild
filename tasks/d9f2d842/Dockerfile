FROM ubuntu:22.04

# Labels
LABEL Author="database-exercise"
LABEL Description="Initial state for Database Dumps Cleanup task"

# Update package list and install Python + Pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create working directory structure expected by the exercise
RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/db_dumps

# Create customers.sql
RUN cat > /home/user/db_dumps/customers.sql <<'EOF'
-- Dump of table customers
INSERT INTO customers (id, name, email) VALUES
(1, 'Alice Smith', 'alice@example.com'),
(2, 'Bob Jones', 'bob@example.com');
EOF

# Create orders.sql
RUN cat > /home/user/db_dumps/orders.sql <<'EOF'
-- Dump of table orders
INSERT INTO orders (id, customer_id, order_total) VALUES
(1, 1, 99.99),
(2, 2, 149.49);
EOF

# Create inventory.sql
RUN cat > /home/user/db_dumps/inventory.sql <<'EOF'
-- Dump of table inventory
INSERT INTO inventory (id, product_name, quantity) VALUES
(1, 'Widget', 500),
(2, 'Gadget', 300);
EOF

# Set read/write permissions so the exercise participant can manipulate files
RUN chmod -R a+rwX /home/user/db_dumps

# Set working directory
WORKDIR /home/user

# Default command
CMD echo "Container for Database Dumps Cleanup exercise." && \
    echo "Navigate to /home/user to begin the task." && \
    /bin/bash