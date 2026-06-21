FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create user home directory
RUN mkdir -p /home/user

# Create directory and JSON fixtures
RUN mkdir -p /home/user/api_responses

RUN cat > /home/user/api_responses/response_1.json <<'EOF'
{
  "id": 101,
  "status": "OK",
  "latency_ms": 234
}
EOF

RUN cat > /home/user/api_responses/response_2.json <<'EOF'
{
  "id": 102,
  "status": "FAIL",
  "latency_ms": 678
}
EOF

RUN cat > /home/user/api_responses/response_3.json <<'EOF'
{
  "id": 103,
  "status": "OK",
  "latency_ms": 345
}
EOF

# Fix permissions
RUN chmod 755 /home/user && \
    chmod 644 /home/user/api_responses/response_*.json

ENV PYTHONUNBUFFERED=1

# Help / labels as comments
# Author: apptainer-setup
# Description: Base image for API integration test assignment with pytest pre-installed.

LABEL Author="apptainer-setup" \
      Description="Base image for API integration test assignment with pytest pre-installed."