FROM ubuntu:22.04

# Labels
LABEL Author="migration-task-setup"
LABEL Description="Initial state for the Kubernetes migration plan exercise."

# 1. Basic tooling and Python environment for pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends \
        python3 \
        python3-pip \
        locales && \
    pip3 install --no-cache-dir pytest

# 2. Create required directory tree
RUN mkdir -p /home/user/migration

# Create prod_services.csv
RUN cat > /home/user/migration/prod_services.csv <<'EOF'
service_id,service_name,current_env,replicas,owner
svc-101,auth-service,production,3,team-login
svc-102,billing-service,production,2,team-payment
svc-103,search-service,production,4,team-search
EOF

# Create staging_services.csv
RUN cat > /home/user/migration/staging_services.csv <<'EOF'
service_id,service_name,current_env,replicas,owner
svc-201,auth-service,staging,1,team-login
svc-202,billing-service,staging,1,team-payment
EOF

# Create new_cluster_ips.txt
RUN cat > /home/user/migration/new_cluster_ips.txt <<'EOF'
10.240.0.10
10.240.0.11
10.240.0.12
10.240.0.13
10.240.0.14
EOF

# 3. Ensure write access for the eventual non-root container user
RUN chmod -R 0777 /home/user

# Set working directory
WORKDIR /home/user

# Default command
CMD ["/bin/bash"]