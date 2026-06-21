FROM ubuntu:22.04

# Labels
LABEL Author="data-prep-template"
LABEL Description="Environment for the sales data cleaning task: provides raw_sales.csv and pytest."

# Install system packages and pytest
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create project directory structure
RUN mkdir -p /home/user/datasets && \
    mkdir -p /home/user/logs && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/datasets && \
    chmod 0755 /home/user/logs

# Populate the raw_sales.csv file
RUN cat > /home/user/datasets/raw_sales.csv <<'EOF'
order_id,order_date,region,sales
A001,2020-01-02,North,100.50
A002,2020/01/05,South,200
A003,2020-01-07,,150
,2020-01-10,East,250.75
A005,2020-01-12,West,
EOF

RUN chmod 0644 /home/user/datasets/raw_sales.csv

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user

CMD echo "Container for sales data cleaning task." && \
    echo "Raw data: /home/user/datasets/raw_sales.csv" && \
    echo "Work in /home/user and create the required artefacts as per instructions."