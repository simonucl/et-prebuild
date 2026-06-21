FROM ubuntu:22.04

# Labels
LABEL Author="monitoring-task-prep"
LABEL Description="Sets up initial filesystem state and installs pytest for monitoring package audit task."

# Post installation
RUN set -e && \
    echo "Installing Python and pytest ..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    echo "Preparing directory structure and seed files ..." && \
    install -d -m 0777 /home/user && \
    install -d -m 0777 /home/user/repo && \
    install -d -m 0777 /home/user/installed

# Populate package_inventory.csv
RUN cat > /home/user/repo/package_inventory.csv <<'EOF'
htop,3.2.2
sysstat,12.5.4
iftop,1.0pre4
net-tools,2.10
glances,3.3.0
EOF

RUN chmod 0666 /home/user/repo/package_inventory.csv

# Populate installed_packages.txt
RUN cat > /home/user/installed/installed_packages.txt <<'EOF'
bash,5.0
coreutils,8.30
glances,3.3.0
EOF

RUN chmod 0666 /home/user/installed/installed_packages.txt

# Ensure /home/user/alerts is NOT present at build time
RUN if [ -d /home/user/alerts ]; then \
        rm -rf /home/user/alerts; \
    fi && \
    echo "Container setup complete."

# Environment variables
ENV PYTHONIOENCODING=UTF-8
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set permissions on /home/user at runtime
RUN chmod 755 /home/user