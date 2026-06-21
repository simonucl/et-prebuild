# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer %labels
LABEL Author="ChatGPT"
LABEL Description="Container for Kubernetes manifest inventory task. Provides baseline YAML files and pytest for verification."

# Environment variables from %environment
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONIOENCODING=utf-8

# Install Python, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare baseline exercise files and directories
RUN set -e && \
    mkdir -p /home/user/manifests && \
    chmod 755 /home/user /home/user/manifests

# deployment-frontend.yaml
RUN cat >/home/user/manifests/deployment-frontend.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: nginx
          image: nginx:1.19
EOF

# deployment-backend.yaml
RUN cat >/home/user/manifests/deployment-backend.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: python
          image: python:3.9
EOF

# service-frontend.yaml
RUN cat >/home/user/manifests/service-frontend.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: default
spec:
  selector:
    app: frontend
  ports:
    - port: 80
      targetPort: 80
EOF

# service-backend.yaml
RUN cat >/home/user/manifests/service-backend.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: default
spec:
  selector:
    app: backend
  ports:
    - port: 8000
      targetPort: 8000
EOF

# configmap-app.yaml
RUN cat >/home/user/manifests/configmap-app.yaml <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  LOG_LEVEL: "info"
EOF

# Ensure correct permissions
RUN chmod 644 /home/user/manifests/*.yaml

# Help text from Apptainer %help
# This container supplies the initial environment for the deployment
# inventory exercise. It contains:
#   • /home/user/manifests/ with five YAML manifest files
#   • pytest pre-installed for automated grading