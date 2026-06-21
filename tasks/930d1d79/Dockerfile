FROM ubuntu:22.04

# Author: API-backup exercise container
# This container provides the initial environment for the “API backup” exercise.
# Contains:
#   • /home/user/api_samples/ with three predefined JSON files
#   • pytest installed for automated checking
# Students will create additional artefacts during runtime.

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user && \
    mkdir -p /home/user/api_samples

RUN cat > /home/user/api_samples/sample1.json <<'EOF'
{
  "id": 1,
  "status": "ok",
  "data": "alpha"
}
EOF

RUN cat > /home/user/api_samples/sample2.json <<'EOF'
{
  "id": 2,
  "status": "ok",
  "data": "beta"
}
EOF

RUN cat > /home/user/api_samples/sample3.json <<'EOF'
{
  "id": 3,
  "status": "ok",
  "data": "gamma"
}
EOF

RUN chmod 755 /home/user/api_samples && \
    chmod 644 /home/user/api_samples/sample*.json

LABEL Author="API-backup exercise container"