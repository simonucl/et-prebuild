FROM ubuntu:22.04

# Base packages and Python tooling
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create initial ETL pipeline directory structure and contents
RUN mkdir -p /home/user/etl_pipeline/data/raw
RUN mkdir -p /home/user/etl_pipeline/scripts
RUN mkdir -p /home/user/etl_pipeline/config

RUN chmod 0755 /home/user
RUN find /home/user/etl_pipeline -type d -exec chmod 0755 {} \;

# customers.csv
RUN cat > /home/user/etl_pipeline/data/raw/customers.csv <<'EOF'
id,name,signup_date
1,Alice,2020-01-05
2,Bob,2021-03-12
EOF

# transactions.csv
RUN cat > /home/user/etl_pipeline/data/raw/transactions.csv <<'EOF'
id,customer_id,amount,transaction_date
1001,1,250.75,2022-11-10
1002,2,99.99,2022-11-11
EOF

# extract.sh
RUN cat > /home/user/etl_pipeline/scripts/extract.sh <<'EOF'
#!/usr/bin/env bash
echo "Extract step placeholder"
EOF
RUN chmod 0755 /home/user/etl_pipeline/scripts/extract.sh

# transform.py
RUN cat > /home/user/etl_pipeline/scripts/transform.py <<'EOF'
# Minimal transform script
print("Transform step placeholder")
EOF

# pipeline.yaml
RUN cat > /home/user/etl_pipeline/config/pipeline.yaml <<'EOF'
pipeline:
  name: poc_etl
  schedule: "@daily"
EOF

# Set permissions for data/config files
RUN find /home/user/etl_pipeline -type f ! -name 'extract.sh' -exec chmod 0644 {} \;

RUN apt-get clean

# Environment equivalent
RUN chmod 755 /home/user

# Labels
LABEL Author="Apptainer Task Auto-Generator"
LABEL Description="Environment with pre-populated ETL pipeline and pytest installed for automated grading."

# Help text as comments
# This container provides the initial state required for the ETL backup assignment.
# It contains the /home/user/etl_pipeline directory tree with sample data and
# has pytest installed so the grading system can validate your work.

# Run script (comment only)
# Container for ETL backup assignment. Execute your backup commands after shelling into the container.

CMD ["/bin/bash"]