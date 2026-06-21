FROM ubuntu:22.04

# Labels
LABEL Author="container-security-solution"
LABEL Description="Environment pre-populated with micro-service repo and pytest."

# Install dependencies
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates \
        curl \
        gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install pytest for the grader
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Create the initial repository structure expected by the tests
RUN mkdir -p /home/user/app/service-a && \
    mkdir -p /home/user/app/service-b

# service-a Dockerfile
RUN cat >/home/user/app/service-a/Dockerfile <<'EOF'
FROM python:3.10-slim
COPY . /app
RUN pip install -r requirements.txt
EOF

# service-b Dockerfile
RUN cat >/home/user/app/service-b/Dockerfile <<'EOF'
FROM node:18
ADD . /usr/src/app
RUN npm install
EOF

# Set permissions so that the (non-root) runtime user can create
# additional files/directories under /home/user
RUN chmod -R a+rX /home/user && \
    chmod 0777 /home/user

# Environment variables
ENV PATH="/usr/local/bin:$PATH"

WORKDIR /home/user