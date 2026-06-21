FROM ubuntu:22.04

# Ensure Python and pip are on the PATH
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Update package index and install Python with pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create /home/user/data directory structure
RUN mkdir -p /home/user/data

# Create the canonical CSV file with the required contents
RUN cat > /home/user/data/transactions_2021-12-31.csv <<'EOF'
transaction_id,user_id,amount,currency
T1001,U23,150.00,USD
T1002,U19,75.50,USD
T1003,U11,20.00,EUR
T1004,U23,125.00,USD
EOF

# Set sensible permissions: directories 755, files 644
RUN chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 644 /home/user/data/transactions_2021-12-31.csv

# Default command opens a shell
CMD ["/bin/bash"]

# Help:
# This container provides the initial state for the audit-trail task.
# It contains:
#   • /home/user/data/transactions_2021-12-31.csv  (canonical source CSV)
# Python 3 and pytest are pre-installed for automated grading.