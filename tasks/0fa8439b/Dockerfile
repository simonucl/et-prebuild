FROM ubuntu:22.04

# From %labels
# chmod 755 /home/user
# Author  edge-task-prep

# Create home directory
RUN mkdir -p /home/user

ENV IOT_DIR=/home/user/iot
ENV DEPLOY_DIR=/home/user/iot/deploy

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p "${DEPLOY_DIR}"

RUN cat > "${IOT_DIR}/inventory.csv" <<'EOF'
device01,edge-lab,68,45,ok
device02,edge-lab,77,50,ok
device03,edge-lab,72,85,ok
device04,field,80,90,error
device05,field,60,40,ok
EOF

RUN cat > "${DEPLOY_DIR}/config.ini" <<'EOF'
[deployment]
device_group=edge
version=1.4.2
EOF

RUN chmod -R a+rwX /home/user

# From %help
# This container provides the starting environment for the IoT edge-computing
# task. The initial resources are placed under /home/user/iot/, and pytest is installed.