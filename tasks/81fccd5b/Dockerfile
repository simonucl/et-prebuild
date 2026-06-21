# Author: Task Preparation Script
# Description: Apptainer image for the API-response filtering assignment.
# Help:
# This container provides the initial filesystem state for the “API-response filtering” task.
# It includes:
#   • /home/user/api_responses/orders.json – the raw API response file.
#   • /home/user/output/ – empty, writable directory for results.
# Python 3 and pytest are installed so the automated test-suite can run inside the container.

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    jq \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/api_responses && \
    mkdir -p /home/user/output && \
    chmod 777 /home/user/output

RUN mkdir -p /home/user/api_responses && \
    cat > /home/user/api_responses/orders.json << 'EOF'
[
  {
    "id": 3,
    "customer_name": "Alice Smith",
    "total": 129.99,
    "items": ["SKU_123", "SKU_456"]
  },
  {
    "id": -7,
    "customer_name": "Bob Jones",
    "total": 59.00,
    "items": ["SKU_789"]
  },
  {
    "id": 2,
    "customer_name": "Charlie Doe",
    "items": ["SKU_111", "SKU_222"]
  },
  {
    "id": 5,
    "customer_name": "Dana Roe",
    "total": 0,
    "items": ["SKU_333"]
  },
  {
    "id": 4,
    "customer_name": "Evan Poe",
    "total": -10.50,
    "items": ["SKU_444", "SKU_555"]
  }
]
EOF

RUN chmod 644 /home/user/api_responses/orders.json

RUN mkdir -p /home/user && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8