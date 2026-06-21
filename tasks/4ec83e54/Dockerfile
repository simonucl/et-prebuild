FROM ubuntu:22.04

# Update package lists and install required software
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        rsync \
        --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /opt/remote_manifests && \
    chmod 755 /opt /opt/remote_manifests

# configmap.yaml
RUN cat > /opt/remote_manifests/configmap.yaml <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
EOF

# deployment.yaml
RUN cat > /opt/remote_manifests/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
EOF

# service.yaml
RUN cat > /opt/remote_manifests/service.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
EOF

# Create /home/user
RUN mkdir -p /home/user && chmod 777 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Apply chmod from %environment (must be RUN, not ENV)
RUN chmod 755 /home/user