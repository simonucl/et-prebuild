FROM ubuntu:22.04

# Labels
LABEL Author="dev"
LABEL Description="Environment for the 'Merge CSV data, apply date-filter, convert to JSON' task. Provides input CSV fixtures and pytest."

# Help section as comments
# This container image sets up the initial state expected by the grading
# framework for the CSV-merging exercise. It pre-installs pytest and ships the
# two required input CSV files under:
#   /home/user/projects/api_test/input

# Install Python tooling and pytest
RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create the required input directory tree
RUN mkdir -p /home/user/projects/api_test/input

# Create orders.csv
RUN cat > /home/user/projects/api_test/input/orders.csv <<'EOF'
order_id,customer_id,order_date,amount
1001,C001,2023-01-05,250.75
1002,C002,2023-01-17,400.00
1003,C001,2023-02-03,125.50
1004,C003,2023-03-12,98.00
EOF

# Create customers.csv
RUN cat > /home/user/projects/api_test/input/customers.csv <<'EOF'
customer_id,name,country
C001,Alice Smith,USA
C002,Bob Jones,Canada
C003,Carla Ruiz,Mexico
EOF

# Ensure world-readable permissions so the non-root runtime user can access them
RUN chmod 755 /home /home/user /home/user/projects /home/user/projects/api_test /home/user/projects/api_test/input && \
    chmod 644 /home/user/projects/api_test/input/orders.csv /home/user/projects/api_test/input/customers.csv

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"