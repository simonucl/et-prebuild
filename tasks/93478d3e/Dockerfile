FROM ubuntu:22.04

# Labels
LABEL Author="YourName"
LABEL Description="Container providing initial state for FinOps cost-summary task."

# Install Python3, pip and pytest
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the initial filesystem state expected by the grader
# Base directories
RUN mkdir -p /home/user/cloud_costs/raw

# sep1.csv
RUN cat > /home/user/cloud_costs/raw/sep1.csv <<'EOF'
service,region,amount
EC2,us-east-1,120.50
S3,us-east-1,30.00
Lambda,us-east-1,10.50
EOF

# sep2.csv
RUN cat > /home/user/cloud_costs/raw/sep2.csv <<'EOF'
service,region,amount
EC2,us-east-1,100.00
S3,us-east-1,25.00
RDS,us-east-1,80.00
EOF

# sep3.csv
RUN cat > /home/user/cloud_costs/raw/sep3.csv <<'EOF'
service,region,amount
EC2,us-west-2,90.00
S3,us-west-2,20.00
RDS,us-west-2,60.00
EOF

# Give wide permissions so the non-root runtime user can manipulate files
RUN chmod -R 777 /home/user/cloud_costs && \
    chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1

# Default command
CMD echo "Container for FinOps cost-summary task." && echo "Run your analysis script or open a shell."