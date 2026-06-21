FROM ubuntu:22.04

# Install Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-venv \
        python3-pip \
        python-is-python3 && \
    ln -sf /usr/bin/python3 /usr/local/bin/python && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial workspace expected by the exercise
RUN mkdir -p /home/user/cloud_data

# Create the cost data CSV file
RUN cat > /home/user/cloud_data/cost_data.csv <<'EOF'
Service,Date,CostUSD
EC2,2023-07-01,25.50
S3,2023-07-01,5.25
RDS,2023-07-01,12.00
EC2,2023-07-02,30.75
S3,2023-07-02,4.75
RDS,2023-07-02,11.25
EC2,2023-07-03,28.00
S3,2023-07-03,6.00
EOF

# Make sure the learner (runtime UID/GID) can freely write under /home/user
RUN chmod -R a+rwx /home/user

# Set environment variables
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

WORKDIR /home/user

# Default command
CMD ["echo", "Docker container for the FinOps cost-analysis exercise."]