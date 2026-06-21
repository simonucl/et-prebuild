FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create base directory structure
RUN mkdir -p /home/user/configs/nginx && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/configs && \
    chmod 0755 /home/user/configs/nginx

# Create app.conf
RUN cat > /home/user/configs/app.conf <<'EOF'
# Application configuration
port=8080
debug=true
EOF

# Create db.yml
RUN cat > /home/user/configs/db.yml <<'EOF'
database:
  host: localhost
  port: 5432
  user: app
  password: secret
EOF

# Create nginx.conf
RUN cat > /home/user/configs/nginx/nginx.conf <<'EOF'
user www-data;
worker_processes auto;
events { worker_connections 1024; }
http {
    server {
        listen 80;
        location / {
            proxy_pass http://127.0.0.1:8080;
        }
    }
}
EOF

# Set required permissions
RUN chmod 0644 /home/user/configs/app.conf && \
    chmod 0644 /home/user/configs/db.yml && \
    chmod 0644 /home/user/configs/nginx/nginx.conf

# Set environment
ENV HOME=/home/user

CMD ["sh", "-c", "echo 'Container built for the configuration-backup exercise.' && echo 'Use your own script inside the container to perform the task.'"]