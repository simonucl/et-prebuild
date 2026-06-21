FROM ubuntu:22.04

# Update APT and install Python + Pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the initial directory tree expected by the grading harness
RUN mkdir -p /home/user/provision/templates/app && \
    mkdir -p /home/user/provision/templates/db && \
    mkdir -p /home/user/provision/templates/web

# Populate the template files with the exact required contents
# (including trailing newlines).

# Create app.conf.template
RUN cat > /home/user/provision/templates/app/app.conf.template <<'EOF'
APP_ENV=production
PORT=8080
EOF

# Create db.conf.template
RUN cat > /home/user/provision/templates/db/db.conf.template <<'EOF'
DB_HOST=localhost
DB_PORT=5432
EOF

# Create nginx.conf.template
RUN cat > /home/user/provision/templates/web/nginx.conf.template <<'EOF'
server {
    listen 80;
    server_name example.com;
}
EOF

# Permissions: make sure the executing (non-root) user can create
# new files/directories under /home/user/provision while keeping the
# template files themselves read-only.
RUN chmod 777 /home/user && \
    chmod 777 /home/user/provision && \
    chmod 755 /home/user/provision/templates && \
    find /home/user/provision/templates -type d -exec chmod 755 {} \; && \
    find /home/user/provision/templates -type f -exec chmod 644 {} \;

# Clean up APT caches to keep image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

LABEL Author="YourName"
LABEL Description="Base image for provisioning-templates task—includes template files and pytest."