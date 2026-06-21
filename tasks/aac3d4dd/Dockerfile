FROM ubuntu:22.04

# Labels
LABEL Author="hostname-migration-setup"
LABEL Description="Container image prepared for the hostname migration task"

# Install Python, pip and pytest (needed by the provided test suite)
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial directory structure under /home/user
RUN mkdir -p /home/user/projects/microservices/serviceA/config && \
    mkdir -p /home/user/projects/microservices/serviceA/scripts && \
    mkdir -p /home/user/projects/microservices/serviceB/config && \
    mkdir -p /home/user/projects/microservices/serviceB/scripts && \
    mkdir -p /home/user/projects/microservices/serviceC/config && \
    mkdir -p /home/user/projects/microservices/serviceC/scripts

# Populate *.conf files with the legacy hostname exactly as described
RUN cat > /home/user/projects/microservices/serviceA/config/app.conf <<'EOF'
DB_HOST=legacy.internal.example.com
CACHE_HOST=legacy.internal.example.com
EOF

RUN cat > /home/user/projects/microservices/serviceA/config/db.conf <<'EOF'
jdbc=postgres://legacy.internal.example.com:5432/prod
EOF

RUN cat > /home/user/projects/microservices/serviceB/config/web.conf <<'EOF'
upstream legacy.internal.example.com;
EOF

RUN cat > /home/user/projects/microservices/serviceB/config/cache.conf <<'EOF'
cache_server=legacy.internal.example.com
metrics_host=legacy.internal.example.com
backup_host=legacy.internal.example.com
EOF

RUN cat > /home/user/projects/microservices/serviceC/config/worker.conf <<'EOF'
queue=amqp://legacy.internal.example.com
EOF

# Populate helper scripts
RUN cat > /home/user/projects/microservices/serviceA/scripts/deploy.sh <<'EOF'
#!/bin/sh
echo "deploy"
EOF

RUN cat > /home/user/projects/microservices/serviceB/scripts/restart.sh <<'EOF'
#!/bin/sh
echo "restart"
EOF

RUN cat > /home/user/projects/microservices/serviceC/scripts/cleanup.sh <<'EOF'
#!/bin/sh
echo "cleanup"
EOF

RUN chmod +x \
    /home/user/projects/microservices/serviceA/scripts/deploy.sh \
    /home/user/projects/microservices/serviceB/scripts/restart.sh \
    /home/user/projects/microservices/serviceC/scripts/cleanup.sh

# Set file modification timestamps to control "age" for later tests
RUN touch -d "30 days ago" /home/user/projects/microservices/serviceA/scripts/deploy.sh && \
    touch -d "20 days ago" /home/user/projects/microservices/serviceB/scripts/restart.sh && \
    touch -d "91 days ago" /home/user/projects/microservices/serviceC/scripts/cleanup.sh

# Ensure everything is readable/writable by an unprivileged user
RUN chmod -R u+rwX,go+rX /home/user || true && \
    chmod 755 /home/user

WORKDIR /home/user

CMD ["sh", "-c", "echo 'This container is prepared for the hostname migration exercise.' && echo 'Run your migration commands inside the container shell.'"]