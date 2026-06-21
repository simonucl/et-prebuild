FROM ubuntu:22.04

# Install Python and pytest
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Create required directories
RUN mkdir -p /home/user/source_configs

RUN cat > /home/user/source_configs/config1.yaml <<'EOF'
---
service: web
replicas: 3
EOF

RUN cat > /home/user/source_configs/config2.ini <<'EOF'
[database]
host = db.internal
port = 5432
EOF

RUN cat > /home/user/source_configs/app.env <<'EOF'
APP_ENV=production
DEBUG=false
EOF

# Permissions
RUN chmod 0777 /home/user && \
    chmod 0755 /home/user/source_configs && \
    chmod 0644 /home/user/source_configs/*

# Match %environment section behavior
RUN chmod 755 /home/user
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Labels
LABEL Author="OpenAI ChatGPT"
LABEL Description="Apptainer image for backup-creation task. Provides initial source files and installs pytest."

CMD ["bash"]