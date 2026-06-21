FROM ubuntu:22.04

# Update and install required packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates \
        build-essential

# Install Python packages
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest jsonschema

# Create initial directory structure
RUN mkdir -p /home/user/data

# Create orders.json
RUN cat <<'EOF' > /home/user/data/orders.json
{
  "orders": [
    { "id": 1, "customer": { "name": "Alice", "email": "alice@example.com" }, "total": 250.00, "status": "processed" },
    { "id": 2, "customer": { "name": "Bob", "email": "bob@example.com" }, "total": 65.50,  "status": "pending"   },
    { "id": 3, "customer": { "name": "Carol", "email": "carol@example.com" }, "total": 120.00, "status": "processed" },
    { "id": 4, "customer": { "name": "Dave", "email": "dave@example.com" },  "total": 85.00,  "status": "processed" }
  ]
}
EOF

# Create order_schema.json
RUN cat <<'EOF' > /home/user/data/order_schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["orders"],
  "properties": {
    "orders": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "customer", "total", "status"],
        "properties": {
          "id": { "type": "integer" },
          "customer": {
            "type": "object",
            "required": ["name", "email"],
            "properties": {
              "name":  { "type": "string" },
              "email": { "type": "string", "format": "email" }
            }
          },
          "total":  { "type": "number" },
          "status": { "type": "string" }
        }
      }
    }
  }
}
EOF

# Ensure correct permissions (0644 for files, 0755 for directories)
RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/data && \
    chmod 0644 /home/user/data/orders.json /home/user/data/order_schema.json

# Clean up apt caches to keep the image lean
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

LABEL Author="example"
LABEL Description="Environment for JSON schema validation + jq extraction exercise"

# Help information:
# This container provides an initial working directory with JSON data and schema
# for the student exercise.  Tools installed:
#   • jq           – for JSON processing
#   • jsonschema   – Python implementation of JSON-Schema validation
#   • pytest       – required for automated grading