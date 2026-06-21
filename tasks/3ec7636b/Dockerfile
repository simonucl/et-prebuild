FROM ubuntu:22.04

# Help / metadata
# Author="Apptainer exercise preparation"
# Description="Provision initial state for microservices config-backup task. Installs pytest and pre-populates the /home/user/projects/microservices tree."

ENV HOME=/home/user

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /home/user/projects/microservices/serviceA \
             /home/user/projects/microservices/serviceB \
             /home/user/projects/microservices/serviceC && \
    printf "version: 'A'\n"                         > /home/user/projects/microservices/serviceA/deploy.yaml && \
    printf "SERVICE=serviceA\nDB=mysql\n"           > /home/user/projects/microservices/serviceA/.env && \
    printf "Service A documentation\n"              > /home/user/projects/microservices/serviceA/readme.txt && \
    printf "service: B\nreplicas: 3\n"              > /home/user/projects/microservices/serviceB/app.yaml && \
    printf "SERVICE=serviceB\nDB=postgres\n"        > /home/user/projects/microservices/serviceB/.env && \
    printf "infra: true\nregion: us-east-1\n"       > /home/user/projects/microservices/serviceC/infra.yaml && \
    printf "SERVICE=serviceC\nDB=mongodb\n"         > /home/user/projects/microservices/serviceC/.env && \
    find /home/user/projects -type d -exec chmod 0777 {} \; && \
    find /home/user/projects -type f -exec chmod 0666 {} \; && \
    unset DEBIAN_FRONTEND

CMD ["/bin/bash"]