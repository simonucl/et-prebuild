FROM ubuntu:22.04

# Author example
# Description: Environment for Kubernetes manifest rendering exercise
# This container supplies the initial state for the Kubernetes manifest
# rendering task. pytest is pre-installed for validation.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/k8s/templates && \
    mkdir -p /home/user/k8s/env

RUN cat > /home/user/k8s/templates/deployment.yaml.tpl <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      containers:
        - name: ${APP_NAME}
          image: "docker.io/library/${APP_NAME}:${IMAGE_TAG}"
          env:
            - name: ENVIRONMENT
              value: ${ENVIRONMENT}
EOF

RUN cat > /home/user/k8s/env/.env <<'EOF'
APP_NAME=myapp
IMAGE_TAG=v1.2.3
ENVIRONMENT=production
EOF

RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/k8s && \
    chmod 644 /home/user/k8s/templates/deployment.yaml.tpl && \
    chmod 644 /home/user/k8s/env/.env

ENV HOME=/home/user

LABEL Author="example" \
      Description="Environment for Kubernetes manifest rendering exercise"