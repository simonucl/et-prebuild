FROM ubuntu:22.04

# Install Python and Pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial filesystem state for the student task
RUN mkdir -p /home/user/service_configs

RUN cat > /home/user/service_configs/httpd.conf.orig <<'EOF'
# Example Apache HTTPD Configuration
ServerRoot "/usr/local/apache2"
Listen 80
LoadModule mpm_event_module modules/mod_mpm_event.so
User daemon
Group daemon
ServerTokens Full
ServerSignature On
Options Indexes FollowSymLinks
AllowOverride All
SSLProtocol all -SSLv2 -SSLv3 -TLSv1
Timeout 300
EOF

# Ensure the file ends with exactly one newline character
RUN echo >> /home/user/service_configs/httpd.conf.orig

# Set reasonable permissions so the non-root user can work
RUN chmod -R 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Default command
CMD echo "Container for Apache hardening task." && echo "You can begin your work now."