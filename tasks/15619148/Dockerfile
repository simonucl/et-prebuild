FROM ubuntu:22.04

# Basic development tooling
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    ln -s /usr/bin/python3 /usr/local/bin/python || true

# Python packages required for the test-suite
RUN pip3 install --no-cache-dir pytest

# Pre-populate filesystem with sample JSON payload
RUN mkdir -p /home/user/api_responses && \
    mkdir -p /home/user/work

RUN cat > /home/user/api_responses/orders.json <<'EOF'
[
  { "order_id": 1001, "customer_id": "C001", "total": 123.45, "status": "shipped" },
  { "order_id": 1002, "customer_id": "C002", "total": 67.89,  "status": "processing" },
  { "order_id": 1003, "customer_id": "C003", "total": 250.0,   "status": "delivered"  }
]
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/api_responses && \
    chmod 644 /home/user/api_responses/orders.json && \
    chmod 777 /home/user/work

# Environment
ENV PYTHONUNBUFFERED=1

# Run script equivalent
CMD echo "Container for the Orders endpoint exercise. Open a shell or execute your script."