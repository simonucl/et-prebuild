FROM ubuntu:22.04

# Install Python, pip, pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create initial filesystem state
RUN mkdir -p /home/user/source_data

# customers.csv
RUN cat > /home/user/source_data/customers.csv <<'EOF'
id,name
1,Alice
2,Bob
EOF

# orders.csv
RUN cat > /home/user/source_data/orders.csv <<'EOF'
order_id,customer_id,total
1001,1,250.00
1002,2,175.50

EOF

# products.csv
RUN cat > /home/user/source_data/products.csv <<'EOF'
product_id,name,price
10,Widget,25.00
20,Gadget,40.00
EOF

# Permissions
RUN chmod -R a+rwx /home/user && chmod 755 /home/user

# Labels
LABEL Author="Container prepared for ETL archiving exercise"