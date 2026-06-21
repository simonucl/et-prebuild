FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the exercise
RUN mkdir -p /home/user/server_configs && \
    mkdir -p /home/user/change_logs

# app.yaml (5 lines, each ending with '\n')
RUN cat > /home/user/server_configs/app.yaml <<'EOF'
server:
  host: 0.0.0.0
  port: 8080
  debug: true
  maintenance: false
EOF

# db.toml (6 lines, each ending with '\n')
RUN cat > /home/user/server_configs/db.toml <<'EOF'
[database]
user = "admin"
password = "oldpass"
host = "localhost"
port = 5432
max_connections = 100
EOF

# Ensure the agent (non-root user at runtime) can read/write as required
RUN chmod -R 777 /home/user/server_configs && \
    chmod -R 777 /home/user/change_logs && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8