FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT – Apptainer setup for AWS FinOps CSV task"

# Update APT and install Python + pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory structure
RUN mkdir -p /home/user/raw_reports

# Populate the first raw CSV file
RUN cat > /home/user/raw_reports/aws_costs_2023-08.csv <<'EOF'
Date,Account,Service,Region,CostUSD
2023-08-01,123456789012,AmazonEC2,us-east-1,25.30
2023-08-01,123456789012,AmazonS3,us-east-1,3.76
2023-08-02,123456789012,AmazonEC2,us-east-1,26.10
2023-08-02,123456789012,AmazonS3,us-east-1,3.59
2023-08-03,123456789012,AmazonEC2,us-east-1,24.87
2023-08-03,123456789012,AmazonRDS,us-east-1,14.05
2023-08-03,123456789012,AmazonLambda,us-east-1,1.22
EOF

# Populate the second raw CSV file
RUN cat > /home/user/raw_reports/aws_costs_2023-09.csv <<'EOF'
Date,Account,Service,Region,CostUSD
2023-09-01,123456789012,AmazonEC2,us-east-1,29.44
2023-09-01,123456789012,AmazonS3,us-east-1,3.85
2023-09-01,123456789012,AmazonRDS,us-east-1,14.71
2023-09-02,123456789012,AmazonEC2,us-east-1,30.02
2023-09-02,123456789012,AmazonS3,us-east-1,3.99
2023-09-02,123456789012,AmazonLambda,us-east-1,1.35
2023-09-03,123456789012,AmazonEC2,us-east-1,28.87
2023-09-03,123456789012,AmazonS3,us-east-1,3.78
EOF

# Ensure the student (non-root runtime user) can read/write in /home/user
RUN chmod -R a+rwX /home/user

# Environment variables
ENV LANG=C
ENV LC_ALL=C

WORKDIR /home/user