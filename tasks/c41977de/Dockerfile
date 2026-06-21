FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest

# Create configs directory
RUN mkdir -p /home/user/configs

# Previous version of the config
RUN cat > /home/user/configs/httpd.conf.prev <<'EOF'
# Apache HTTPD previous config
ServerRoot "/etc/httpd"
Listen 80
Include conf.modules.d/*.conf
User apache
Group apache
EOF

# Current version of the config
RUN cat > /home/user/configs/httpd.conf.curr <<'EOF'
# Apache HTTPD current config
ServerRoot "/etc/httpd"
Listen 80
Listen 8080
Include conf.modules.d/*.conf
User apache
Group apache
EOF

# Set permissions
RUN chmod 0777 /home/user/configs && \
    chmod 0644 /home/user/configs/httpd.conf.prev /home/user/configs/httpd.conf.curr && \
    chmod 0755 /home/user || true

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1