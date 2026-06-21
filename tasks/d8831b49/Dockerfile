FROM ubuntu:22.04

# Labels
LABEL Author="Integration-Dev Exercise"
LABEL Description="Container providing the initial state for the \"offline mock-API\" task."

# System packages
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Python tooling
RUN pip3 install --no-cache-dir pytest

# Prepare initial filesystem for the exercise
RUN mkdir -p /home/user/api_samples && \
    chmod 755 /home/user && \
    chmod 755 /home/user/api_samples

# Create response1.json with the exact canonical representation
RUN cat > /home/user/api_samples/response1.json <<'EOF'
{
  "id": 101,
  "status": "success",
  "elapsed_ms": 123,
  "payload": {
    "result": "OK"
  }
}
EOF

# Create response2.json with the exact canonical representation
RUN cat > /home/user/api_samples/response2.json <<'EOF'
{
  "id": 102,
  "status": "error",
  "elapsed_ms": 456,
  "payload": {
    "result": "FAIL"
  }
}
EOF

# Ensure predictable permissions
RUN chmod 644 /home/user/api_samples/response1.json /home/user/api_samples/response2.json

# Environment variables
ENV PYTHONIOENCODING=utf-8

# Help information (as comment)
# This container image sets up the initial directory layout and files
# required for the "offline mock-API" integration-developer exercise.
# Only pytest is pre-installed for the test harness.