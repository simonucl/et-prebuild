FROM ubuntu:22.04

# Update package index and install Python + pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip

# Install pytest for the test-runner
RUN pip3 install --no-cache-dir pytest

# Create non-root user "user" and the required initial file layout
RUN useradd -m -s /bin/bash user || true

# Directory that the exercise relies on
RUN mkdir -p /home/user/data

# Populate /home/user/data/sales_q1.csv
RUN cat > /home/user/data/sales_q1.csv <<'EOF'
order_id,customer_email,amount
1001,alice@example.com,250.00
1002,bob@gmail.com,175.50
1003,charlie@example.com,300.00
EOF

# Populate /home/user/data/customer_info.csv
RUN cat > /home/user/data/customer_info.csv <<'EOF'
customer_id,name,email,credit_card
c001,Alice Smith,alice@example.com,4111-1111-1111-1111
c002,Bob Johnson,bob@gmail.com,5500-0000-0000-0004
c003,Charlie Brown,charlie@example.com,6011-0009-9013-9424
EOF

# Permissions – allow any non-root user to read and work within /home/user
RUN chown -R user:user /home/user && \
    chmod -R a+rX /home/user

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /home/user