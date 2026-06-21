FROM ubuntu:22.04

# Labels
LABEL Author="audit-task-container"

# Install required packages
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Set up filesystem for the exercise
RUN mkdir -p /home/user/data

# Create transactions.json
RUN cat > /home/user/data/transactions.json <<'EOF'
[
  { "id": "TX1001", "amount": 150.00, "currency": "USD", "status": "approved" },
  { "id": "TX1002", "amount": 200.50, "currency": "EUR" },
  { "id": "TX1003", "amount": 99.99, "currency": "USD", "status": "declined" }
]
EOF

# Create transaction_schema.json
RUN cat > /home/user/data/transaction_schema.json <<'EOF'
{
  "type": "object",
  "required": ["id", "amount", "currency", "status"]
}
EOF

# Set permissions
# Allow non-root users to create /home/user/audit and write files
RUN chmod 0777 /home/user && \
    chmod -R a+rw /home/user/data

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user

CMD ["/bin/bash"]