FROM ubuntu:22.04

# Update package index and install Python + pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create initial directory structure
RUN mkdir -p /home/user/app/config

# Write settings.ini with original secrets
RUN cat > /home/user/app/config/settings.ini <<'EOF'
[database]
user = app_user
password = oldDBpwd123

[api]
key = OLDAPIKEY0987654321

[general]
debug = false
EOF

# Permissions
RUN chmod -R 777 /home/user
RUN chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH