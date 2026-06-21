FROM ubuntu:22.04

# Labels
LABEL Author="cloud-migration-prep"
LABEL Description="Environment prepared for cloud-migration transformation task with pytest pre-installed."

# Post installation
RUN set -e && \
    echo "=== Updating apt cache and installing required packages ===" && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip \
        jq parallel \
        coreutils gawk sed grep \
        ca-certificates && \
    echo "=== Installing pytest via pip ===" && \
    pip3 install --no-cache-dir pytest && \
    echo "=== Creating directory structure ===" && \
    mkdir -p /home/user/cloud_migration/source && \
    mkdir -p /home/user/cloud_migration/output && \
    mkdir -p /home/user/cloud_migration/logs

# Populate canonical services.csv
RUN cat > /home/user/cloud_migration/source/services.csv << 'EOF'
service_name,node,port,protocol,status
auth-api,edge-1,443,https,active
billing-api,edge-2,443,https,active
legacy-report,node-5,8080,http,inactive
user-db,edge-1,5432,postgres,active
cache,node-3,6379,redis,maintenance
frontend,node-2,80,http,active
search,node-2,9200,http,active
EOF

# Set permissions and clean up
RUN echo "=== Setting permissions so non-root user inside the container can write to output & logs ===" && \
    chmod 0755 /home/user && \
    chmod 0755 /home/user/cloud_migration && \
    chmod 0755 /home/user/cloud_migration/source && \
    chmod 0777 /home/user/cloud_migration/output && \
    chmod 0777 /home/user/cloud_migration/logs && \
    chmod 0644 /home/user/cloud_migration/source/services.csv && \
    echo "=== Cleaning up APT lists ===" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV HOME=/home/user

WORKDIR /home/user

# Default command
CMD ["echo", "Container for the cloud-migration data-reshaping task. Use: docker exec <container> <your command>"]