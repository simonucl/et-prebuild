# Converted from Apptainer definition using localimage; using Ubuntu 22.04 as base.
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Create home directory
RUN mkdir -p /home/user

# Install Python and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial deployment tree
RUN mkdir -p /home/user/deployment/configs

# Create initial app.env
RUN cat << 'EOF' > /home/user/deployment/configs/app.env
APP_NAME=SampleApp
APP_VERSION=1.3.4
APP_PORT=8080
EOF

# Create initial db.env
RUN cat << 'EOF' > /home/user/deployment/configs/db.env
DB_NAME=sampledb
DB_HOST=localhost
DB_PORT=5432
DB_USER=sampleuser
DB_PASSWORD=samplepass
EOF

# Ensure permissions
RUN chmod -R a+rwX /home/user && chmod 755 /home/user

# Default runscript equivalent
CMD ["bash"]