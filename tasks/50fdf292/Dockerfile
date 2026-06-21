FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /home/user/k8s/manifests

# deployment.yaml
RUN cat > /home/user/k8s/manifests/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: demo
  template:
    metadata:
      labels:
        app: demo
    spec:
      containers:
      - name: demo
        image: nginx:1.21
EOF

# service.yaml
RUN cat > /home/user/k8s/manifests/service.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: demo-service
spec:
  selector:
    app: demo
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
EOF

# configmap.yaml
RUN cat > /home/user/k8s/manifests/configmap.yaml <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: demo-config
data:
  example.property.1: hello
  example.property.2: world
EOF

# Permissions
RUN chmod -R 755 /home/user && \
    find /home/user/k8s/manifests -type f -exec chmod 644 {} \;

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH