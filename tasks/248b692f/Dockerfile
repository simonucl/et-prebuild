# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python, pip, and dependencies
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create directory structure
RUN mkdir -p /home/user/cloud_costs/raw

# Create the CSV file using heredoc
RUN cat > /home/user/cloud_costs/raw/march_2024_spend.csv <<'EOF'
Date,Account,Service,CostUSD
2024-03-01,Dev,Compute,15.50
2024-03-02,Prod,Compute,25.00
2024-03-03,Dev,Storage,5.25
2024-03-04,Prod,Storage,12.75
2024-03-05,Dev,Database,20.00
2024-03-06,Prod,Database,30.00
2024-03-07,Dev,Networking,7.00
2024-03-08,Prod,Networking,14.00
EOF

# Create results directory and adjust permissions
RUN mkdir -p /home/user/cloud_costs/results && \
    chmod -R a+rwX /home/user/cloud_costs

# Environment setup
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1