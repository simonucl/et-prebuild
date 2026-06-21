FROM ubuntu:22.04

# Labels
LABEL Author="AI-Generated"
LABEL Description="Starting environment for the CSV-processing parallelization task"

# Install system packages
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        parallel \
        ca-certificates \
        locales && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/data/raw && \
    mkdir -p /home/user/data/processed && \
    mkdir -p /home/user/project

# Populate raw CSV files - sales_q1.csv
RUN cat >/home/user/data/raw/sales_q1.csv <<'EOF'
id,region,amount
1,North,1000
2,South,1500
3,East,800
EOF

# Populate raw CSV files - sales_q2.csv
RUN cat >/home/user/data/raw/sales_q2.csv <<'EOF'
id,region,amount
4,North,1100
5,South,1600
6,West,900
EOF

# Populate raw CSV files - sales_q3.csv
RUN cat >/home/user/data/raw/sales_q3.csv <<'EOF'
id,region,amount
7,East,1200
8,West,950
9,North,1300
EOF

# Supply the intentionally faulty processing script
RUN cat >/home/user/project/process_data.sh <<'EOF'
#!/bin/bash
# WRONG: simply concatenates files and duplicates headers
cat /home/user/data/raw/*.csv > /home/user/data/processed/all_sales_2023.csv
echo "done"
EOF

RUN chmod 0777 /home/user/project/process_data.sh

# Ensure the non-root user who will run tests can modify everything
RUN chmod -R 0777 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Runscript equivalent
CMD ["echo", "Container for CSV-processing task. Open a shell to start working."]