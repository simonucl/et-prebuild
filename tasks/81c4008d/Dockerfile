FROM ubuntu:22.04

# Help section (from Apptainer %help if present; none provided)

# Basic utilities and Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        make \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create the unprivileged user and project seed directory structure
RUN useradd -m -s /bin/bash user || true

RUN mkdir -p /home/user/project/data/raw

# Seed raw CSV files
RUN cat > /home/user/project/data/raw/customers.csv <<'EOF'
id,name,email
1,Alice,alice@example.com
2,Bob,
3,,charlie@example.com
4,David,david@example.com
EOF

RUN cat > /home/user/project/data/raw/transactions.csv <<'EOF'
tid,customer_id,amount
1001,1,23.50
1002,2,
1003,3,100.00
1004,4,55.25
EOF

# Set permissions
RUN chmod -R 0777 /home/user && chmod 755 /home/user

# Environment variables
ENV PYTHONIOENCODING=UTF-8

# Default run behavior
CMD ["/bin/bash"]