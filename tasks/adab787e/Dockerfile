FROM ubuntu:22.04

# Labels
LABEL Author="example@example.com"
LABEL Description="Minimal environment for ETL archiving task with pytest installed."

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create a non-root user and its home directory
RUN useradd -m -s /bin/bash user || true

# Prepare the raw_data directory
RUN mkdir -p /home/user/raw_data

# Create customers.csv
RUN cat > /home/user/raw_data/customers.csv <<'EOF'
customer_id,customer_name
1,John Doe
2,Jane Doe
EOF

# Create orders.csv
RUN cat > /home/user/raw_data/orders.csv <<'EOF'
order_id,customer_id,amount
1001,1,250.50
1002,2,450.00
1003,1,125.75
EOF

# Create products.csv
RUN cat > /home/user/raw_data/products.csv <<'EOF'
product_id,product_name
2001,Widget
2002,Gadget
EOF

# Ensure the regular user owns its home directory tree
RUN chown -R user:user /home/user

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV HOME=/home/user

WORKDIR /home/user