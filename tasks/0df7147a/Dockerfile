FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up initial application directory structure and legacy credentials
RUN mkdir -p /home/user/app/config && \
    chmod 777 /home/user/app /home/user/app/config

# Create the legacy credentials file (exact content, NO trailing newline)
RUN printf 'DB_USER=legacyuser\nDB_PASSWORD=L0ngOldPass\nAPI_TOKEN=oldtoken999' > /home/user/app/config/credentials.env && \
    chmod 666 /home/user/app/config/credentials.env

# Set permissions for home directory
RUN chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1