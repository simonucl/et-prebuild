FROM ubuntu:22.04

# Labels
LABEL Author="microstack-task-preparer"
LABEL Description="Container providing initial state for micro-services YAML summarization task"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata \
        git \
        curl && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create initial filesystem expected by the grader
RUN mkdir -p /home/user/microstack/api /home/user/microstack/auth /home/user/microstack/worker

# api/service.yml
RUN cat > /home/user/microstack/api/service.yml <<'EOF'
service: api
image: registry.company.com/api-service:2.1.0
ports:
  - "8081:80"
environment:
  - "AUTH_ENDPOINT=http://auth:80"
  - "CACHE_HOST=redis.internal"
  - "CACHE_PORT=6379"
EOF

# auth/service.yml
RUN cat > /home/user/microstack/auth/service.yml <<'EOF'
service: auth
image: registry.company.com/auth-service:1.4.2
ports:
  - "8080:80"
environment:
  - "DB_HOST=db.internal"
  - "DB_PORT=5432"
  - "JWT_SECRET=supersecret"
EOF

# worker/service.yml
RUN cat > /home/user/microstack/worker/service.yml <<'EOF'
service: worker
image: registry.company.com/worker-service:0.9.3
ports:
  - "8082:80"
environment:
  - "QUEUE_HOST=rabbit.internal"
  - "QUEUE_PORT=5672"
EOF

# Ensure correct permissions (readable by all users)
RUN chmod -R a+rX /home/user

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Container for microstack task. Run your commands inside an interactive shell."]