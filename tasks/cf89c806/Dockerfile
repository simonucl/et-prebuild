FROM ubuntu:22.04

# Labels
LABEL Author="dev-team"
LABEL Description="Environment for compliance audit-trail exercise"

# Help information (as comments):
# This Docker image provides the initial filesystem state and
# tools (Python + pytest) required for the compliance audit-trail
# programming task.

ENV DEBIAN_FRONTEND=noninteractive

# Install Python and pytest (plus minimal tooling)
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create initial filesystem layout for the compliance exercise
RUN mkdir -p /home/user/compliance/raw && \
    mkdir -p /home/user/compliance/audit

# Populate raw CSV files with exact required contents
RUN cat > /home/user/compliance/raw/transactions_20230630.csv << 'EOF'
timestamp,transaction_id,user_id,amount,status
2023-06-30T09:15:44Z,TN001,U1001,250.00,APPROVED
2023-06-30T10:05:37Z,TN002,U1002,145.50,DECLINED
2023-06-30T11:22:08Z,TN003,U1003,980.00,APPROVED
EOF

RUN cat > /home/user/compliance/raw/users.csv << 'EOF'
user_id,user_name
U1001,Alice Huang
U1002,Bob Singh
U1003,Charlie Garcia
EOF

# Set permissions
# Directories: readable and searchable, audit dir also writable
# Files: read-only for others
RUN chmod 755 /home/user && \
    chmod 755 /home/user/compliance && \
    chmod 755 /home/user/compliance/raw && \
    chmod 777 /home/user/compliance/audit && \
    chmod 644 /home/user/compliance/raw/transactions_20230630.csv && \
    chmod 644 /home/user/compliance/raw/users.csv

WORKDIR /home/user