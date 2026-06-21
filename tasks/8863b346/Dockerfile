FROM ubuntu:22.04

# Maintainer information
LABEL Author="CloudArchitect"
LABEL Description="Base image with initial inventory and pytest installed for migration-plan exercise."

# Help text
# This container image provides the starting environment for the
# “service-migration plan” task. It includes:
#   • /home/user/cloud/inventory.csv (pre-populated)
#   • pytest (via pip) for automated validation
# Students will run inside the container without root privileges and
# are expected to create additional artefacts in /home/user/cloud.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/cloud && \
    chmod 0777 /home/user/cloud

RUN cat > /home/user/cloud/inventory.csv <<'EOF'
ServiceName,OldServer,NewServer,Owner
auth-api,vm-auth-01,vm-auth-02,becky
billing-db,vm-db-08,vm-db-new,rahul
frontend,vm-fe-03,vm-fe-blue,carla
metrics,vm-mt-01,vm-mt-02,becky
search,vm-sr-12,vm-sr-green,rahul
EOF

RUN chmod 0644 /home/user/cloud/inventory.csv && \
    chmod 755 /home/user

ENV LC_ALL=C
ENV LANG=C