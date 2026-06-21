FROM ubuntu:22.04

# Help / labels
LABEL Author="Apptainer exercise preparer"
LABEL Description="Container image for the inventory service migration task with pytest installed."

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/app/config

RUN cat > /home/user/app/config/service.conf <<'EOF'
# Service configuration
service_name=inventory
endpoint=old.cloud.internal
port=8080
EOF

RUN chmod 777 /home/user/app && \
    chmod 777 /home/user/app/config && \
    chmod 666 /home/user/app/config/service.conf

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8