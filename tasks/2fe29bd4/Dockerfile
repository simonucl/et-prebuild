FROM ubuntu:22.04

# Author "OpenAI ChatGPT"
# Description "Base image for the FinOps month-end export task. Provides initial CSV data and pytest for automated grading."

ENV DEBIAN_FRONTEND=noninteractive \
    HOME=/home/user

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/incoming_reports && \
    chmod 755 /home/user && \
    chmod 755 /home/user/incoming_reports

RUN cat > /home/user/incoming_reports/aws_costs_2023-09.csv << 'EOF'
service,cost_usd
EC2,25.50
S3,7.25
Lambda,2.40
EOF

RUN cat > /home/user/incoming_reports/azure_costs_2023-09.csv << 'EOF'
service,cost_usd
VM,30.00
Storage,5.75
Functions,1.10
EOF

RUN cat > /home/user/incoming_reports/gcp_costs_2023-09.csv << 'EOF'
service,cost_usd
ComputeEngine,18.60
CloudStorage,6.90
CloudFunctions,0.95
EOF

RUN chmod 644 /home/user/incoming_reports/*.csv