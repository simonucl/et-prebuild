FROM ubuntu:22.04

# Labels
LABEL Author="platform-engineer-task-setup"
LABEL Description="Baseline container for Kubernetes manifest disk-usage reporting task"

# Post section commands
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/k8s/manifests && \
    chmod 0777 /home/user && \
    truncate -s 500  /home/user/k8s/manifests/configmap_env.yaml && \
    truncate -s 2310 /home/user/k8s/manifests/deploy_backend.yaml && \
    truncate -s 1560 /home/user/k8s/manifests/deploy_frontend.yaml && \
    truncate -s 830  /home/user/k8s/manifests/service_backend.yaml && \
    truncate -s 780  /home/user/k8s/manifests/service_frontend.yaml && \
    rm -rf /home/user/k8s-reports

# Commands originally (incorrectly) placed in %environment but not actual env vars
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:${PATH}"