FROM ubuntu:22.04

# Basic tooling: Python + Pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create initial directory structure
RUN mkdir -p /home/user/raw_data && \
    mkdir -p /home/user/processed && \
    mkdir -p /home/user/etl_logs && \
    chmod -R 0777 /home/user

# Populate CSV files
RUN cat > /home/user/raw_data/sales_q1.csv <<'EOF'
order_id,customer_id,order_date,item_count,item_total,discount
1001,C001,2024-01-05,3,120.50,5.00
1002,C002,2024-01-07,1,45.00,0.00
1003,C003,2024-02-18,2,89.99,10.00
1004,C001,2024-03-22,5,300.00,15.00
EOF

RUN cat > /home/user/raw_data/sales_q2.csv <<'EOF'
order_id,customer_id,order_date,item_count,item_total,discount
1005,C003,2024-04-02,1,40.00,0.00
1006,C004,2024-04-11,2,95.00,5.00
1007,C002,2024-05-27,4,180.00,20.00
1008,C003,2024-06-30,3,135.50,10.50
EOF

RUN chmod 0644 /home/user/raw_data/sales_q1.csv /home/user/raw_data/sales_q2.csv

# Environment
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Run script
CMD echo "Container for the sales-summary ETL assignment." && \
    echo "All prerequisite raw data files are located in /home/user/raw_data." && \
    echo "Write your solution so that it produces:" && \
    echo "  • /home/user/processed/customer_summary.csv" && \
    echo "  • /home/user/etl_logs/etl_2024-08-15T00-00-00Z.log" && \
    echo "Good luck!"