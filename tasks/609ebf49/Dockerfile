FROM ubuntu:22.04

# Labels
LABEL Author="security_task_builder"
LABEL Description="Base image for security remediation task – prepares vulnerable webapp and installs pytest"

# Install required OS packages
RUN set -e && \
    echo "##### Install required OS packages #####" && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest

# Create non-privileged user 'user'
RUN echo "##### Create non-privileged user 'user' #####" && \
    groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# Build vulnerable web application tree
RUN echo "##### Build vulnerable web application tree #####" && \
    install -d -m 0755 /home/user/webapp && \
    install -d -m 0777 /home/user/webapp/scripts && \
    install -d -m 0755 /home/user/webapp/config

# Create index.php (0644)
RUN cat >/home/user/webapp/index.php <<'PHP'
<?php
echo "Hello, world!\n";
?>
PHP

RUN chmod 0644 /home/user/webapp/index.php

# Create scripts/deploy.sh (0777 – intentionally insecure)
RUN cat >/home/user/webapp/scripts/deploy.sh <<'SH'
#!/usr/bin/env bash
echo "Deploying application..."
SH

RUN chmod 0777 /home/user/webapp/scripts/deploy.sh

# Create config/settings.ini (0644) with insecure setting
RUN echo "disable-auth = true" >/home/user/webapp/config/settings.ini && \
    chmod 0644 /home/user/webapp/config/settings.ini

# Obsolete identical backup (0644)
RUN cp /home/user/webapp/config/settings.ini /home/user/webapp/config/settings.ini.bak && \
    chmod 0644 /home/user/webapp/config/settings.ini.bak

# Ensure ownership
RUN echo "##### Ensure ownership #####" && \
    chown -R user:user /home/user

# Cleanup APT cache
RUN echo "##### Cleanup APT cache #####" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH=/home/user/.local/bin:$PATH

# Default entrypoint
ENTRYPOINT ["/bin/bash", "-c", "exec \"$@\"", "--"]