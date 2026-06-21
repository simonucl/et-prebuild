FROM ubuntu:22.04

# HELP:
# Author FinOpsTaskSetup
# Description: Container prepared for FinOps analysis challenge – includes raw January 2024 usage CSVs and pytest.

ENV CLOUD_RAW_DIR=/home/user/cloud_usage/raw_logs

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p "$CLOUD_RAW_DIR"

RUN cat > "$CLOUD_RAW_DIR/compute_jan.csv" <<'EOF'
Service,InstanceType,Hours,HourlyCostUSD
EC2,m5.large,200,0.096
EC2,c5.xlarge,150,0.17
Lambda,GB-Seconds,3000000,0.00001667
EOF

RUN cat > "$CLOUD_RAW_DIR/storage_jan.csv" <<'EOF'
Service,GB-Months,CostPerGBMonthUSD
S3 Standard,500,0.023
S3 Glacier,200,0.004
EOF

RUN chmod 755 /home && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/cloud_usage /home/user/cloud_usage/raw_logs && \
    chmod 644 "$CLOUD_RAW_DIR/compute_jan.csv" "$CLOUD_RAW_DIR/storage_jan.csv"