# Converted from Apptainer definition file

FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Automation"
LABEL Description="Environment for Nginx deployment optimization task with pytest pre-installed"

# Environment variables (none were defined in %environment)

# System setup and Python installation
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/deployment/staging && \
    mkdir -p /home/user/deployment/prod

# Create nginx.conf via heredoc
RUN cat >/home/user/deployment/staging/nginx.conf <<'EOF'
user  nginx;
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
    }
}
EOF

# Set permissions
RUN chmod 755 /home/user /home/user/deployment /home/user/deployment/staging /home/user/deployment/prod && \
    chmod 644 /home/user/deployment/staging/nginx.conf

# Equivalent of %runscript (Docker does not use runscript; adding as comments)
# Container for the Nginx deployment optimization task is ready.
# Run your commands or tests inside this container.

CMD echo "Container for the Nginx deployment optimization task is ready." && \
    echo "Run your commands or tests inside this container."