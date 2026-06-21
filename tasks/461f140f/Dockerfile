FROM ubuntu:22.04

# Install Python tooling (pytest + dependencies)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3 && \
    pip3 install --no-cache-dir pytest

# Create initial directory tree and seed files
RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/data/finance/budget && \
    mkdir -p /home/user/data/hr/policies && \
    find /home/user/data -type d -exec chmod 0755 {} \;

# Seed accounts.txt
RUN cat <<'EOF_ACCOUNTS' > /home/user/data/finance/accounts.txt
Quarterly accounts receivable: Q4 2024
Total: 123456
EOF_ACCOUNTS

# Seed 2024_budget.xlsx
RUN cat <<'EOF_BUDGET' > /home/user/data/finance/budget/2024_budget.xlsx
dummy finance spreadsheet
EOF_BUDGET

# Seed employees.csv
RUN cat <<'EOF_EMP' > /home/user/data/hr/employees.csv
id,name,department
1,Alice,HR
2,Bob,HR
EOF_EMP

# Seed leave_policy.md
RUN cat <<'EOF_POLICY' > /home/user/data/hr/policies/leave_policy.md
# Leave Policy
All employees are entitled to 30 days of leave per year.
EOF_POLICY

# Apply file permissions
RUN find /home/user/data -type f -exec chmod 0644 {} \;

# Labels (converted to comments)
# Author backup-admin-challenge
# Description: Container seed for "backup administrator" task. Provides the required initial filesystem state and has pytest pre-installed.

# Help text
# This image contains the expected initial directory tree and files for the backup administrator assignment. Pytest is pre-installed.

# Environment (none required)
ENV HOME=/home/user