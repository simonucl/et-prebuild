FROM ubuntu:22.04

# Author FinOps-Task-Setup
# Description "Base image prepared for FinOps July-2023 multi-cloud cost exercise."

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/raw_costs

RUN cat <<'EOF' > /home/user/raw_costs/aws_july2023.csv
Cloud,Service,Environment,CostUSD
AWS,EC2,Prod,123.45
AWS,S3,Dev,45.67
AWS,RDS,Prod,600.00
AWS,Lambda,Dev,12.34
AWS,DynamoDB,Prod,50.00
EOF

RUN cat <<'EOF' > /home/user/raw_costs/gcp_july2023.csv
Cloud,Service,Environment,CostUSD
GCP,Compute,Prod,200.11
GCP,Storage,Dev,50.00
GCP,BigQuery,Prod,700.00
GCP,CloudFunctions,Dev,30.00
EOF

RUN cat <<'EOF' > /home/user/raw_costs/azure_july2023.csv
Cloud,Service,Environment,CostUSD
Azure,VM,Prod,400.00
Azure,Blob,Dev,80.00
Azure,SQLDB,Prod,650.00
Azure,Functions,Dev,25.00
EOF

RUN chmod -R 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

CMD ["/bin/bash"]