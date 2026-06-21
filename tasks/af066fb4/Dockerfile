FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the "FinOps archive" exercise
# Source data location
RUN mkdir -p /home/user/billing_data

# monthly_2023-07.csv (exactly 102 bytes, including newlines)
RUN cat <<'EOF' > /home/user/billing_data/monthly_2023-07.csv
CostCenter,Service,UsageHours,CostUSD
FinOps,Compute Engine,720,1234.56
FinOps,Cloud Storage,50,12.34
EOF

# monthly_2023-08.csv (exactly 102 bytes, including newlines)
RUN cat <<'EOF' > /home/user/billing_data/monthly_2023-08.csv
CostCenter,Service,UsageHours,CostUSD
FinOps,Compute Engine,744,1250.78
FinOps,Cloud Storage,55,13.89
EOF

# monthly_2023-09.csv (exactly 102 bytes, including newlines)
RUN cat <<'EOF' > /home/user/billing_data/monthly_2023-09.csv
CostCenter,Service,UsageHours,CostUSD
FinOps,Compute Engine,730,1199.99
FinOps,Cloud Storage,60,14.01
EOF

# Ensure world-readable permissions (0644)
RUN chmod 0644 /home/user/billing_data/*.csv

# Make sure the backups directory is absent so tests start clean
RUN if [ -d /home/user/backups ]; then rm -rf /home/user/backups; fi

# Set permissions on home directory
RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /home/user