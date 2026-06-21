FROM ubuntu:22.04

# Base system packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python tooling – pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Prepare initial filesystem state for the exercise
# Create the required raw-data hierarchy
RUN mkdir -p /home/user/data/raw/dataset_A && \
    mkdir -p /home/user/data/raw/dataset_B

# Populate dataset_A CSVs - sample1.csv
RUN cat >/home/user/data/raw/dataset_A/sample1.csv <<'EOF'
gene_id,value
A1,5
A2,7
EOF

# Populate dataset_A CSVs - sample2.csv
RUN cat >/home/user/data/raw/dataset_A/sample2.csv <<'EOF'
gene_id,value
A3,2
A4,9
EOF

# Populate dataset_B CSVs - sample1.csv
RUN cat >/home/user/data/raw/dataset_B/sample1.csv <<'EOF'
gene_id,value
B1,4
B2,1
EOF

# Populate dataset_B CSVs - sample2.csv
RUN cat >/home/user/data/raw/dataset_B/sample2.csv <<'EOF'
gene_id,value
B3,6
B4,3
EOF

# Permissions
# Allow the (non-root) student user to create new directories/files
RUN chmod 777 /home/user && \
    chmod 777 /home/user/data && \
    chmod 644 /home/user/data/raw/dataset_*/sample*.csv

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user