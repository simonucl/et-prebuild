FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user

RUN cat >/home/user/mock_api_response.json <<'EOF'
{
  "original_query": "SELECT * FROM employees",
  "optimized_query": "SELECT id, name, department FROM employees",
  "cost_reduction_percent": 37
}
EOF

RUN chmod 644 /home/user/mock_api_response.json && \
    chmod 777 /home/user

# Environment adjustments
RUN chmod 755 /home/user
ENV PATH="$PATH:/home/user/.local/bin"

# Labels
LABEL Author="task-prep"
LABEL Description="Container for curl file-copy smoke-test task"