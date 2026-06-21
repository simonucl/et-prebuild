FROM ubuntu:22.04

# Labels
LABEL Author="automation_task_builder"
LABEL Description="Environment for the 'quarterly_rollup' Unix-workflow exercise"

# Post installation
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/source_data && \
    mkdir -p /home/user/workflows && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/workflows

# Create sales_q1.csv
RUN cat >/home/user/source_data/sales_q1.csv <<'EOF'
Date,Region,Product,Units,Revenue
2024-01-10,North,Widget,120,2400
2024-02-12,South,Gadget,85,1700
2024-03-08,East,Thingamajig,60,1200
EOF

# Create sales_q2.csv
RUN cat >/home/user/source_data/sales_q2.csv <<'EOF'
Date,Region,Product,Units,Revenue
2024-04-11,North,Widget,130,2600
2024-05-15,South,Gadget,90,1800
2024-06-18,East,Thingamabob,70,1400
EOF

# Set permissions on source_data
RUN chmod 0755 /home/user/source_data && \
    chmod 0644 /home/user/source_data/sales_q*.csv

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user