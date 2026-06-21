FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Auto-Builder"
LABEL Description="Environment for FinOps Makefile task with pytest pre-installed."

# Install necessary packages
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        make \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the FinOps Makefile exercise
RUN mkdir -p /home/user/finops/raw

RUN cat > /home/user/finops/raw/usage_2023-07.csv <<'EOF'
date,service,cost_usd
2023-07-01,Compute,200.00
2023-07-02,Compute,300.00
2023-07-03,Storage,500.00
2023-07-04,Network,23.45
2023-07-05,Compute,500.00
EOF

# Ensure the student (non-root) can write inside /home/user
RUN chmod -R 0777 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Set working directory
WORKDIR /home/user