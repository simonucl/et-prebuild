FROM ubuntu:22.04

# Help text
# This container image provides the initial filesystem state and pytest
# installation required for the micro-services Dockerfile scanning task.

LABEL Author="ContainerPrepBot"
LABEL Description="Base environment for micro-services Dockerfile security scan task"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/microservices/service-a && \
    mkdir -p /home/user/microservices/service-b && \
    mkdir -p /home/user/microservices/service-c && \
    mkdir -p /home/user/scan

RUN cat <<'EOF' > /home/user/microservices/service-a/Dockerfile
FROM python:3.9-slim
# Simple API service
EOF

RUN cat <<'EOF' > /home/user/microservices/service-b/Dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl
EOF

RUN cat <<'EOF' > /home/user/microservices/service-c/Dockerfile
FROM node:14
WORKDIR /usr/src/app
EOF

RUN chmod 0777 /home/user/scan

RUN chmod 755 /home/user

CMD ["/bin/bash"]