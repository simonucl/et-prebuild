FROM ubuntu:22.04

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Labels
LABEL Author="Kubernetes Kind Counter Prep Container"

# Base packages and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /home/user/k8s-configs

# Create backend-deploy.yaml
RUN cat > /home/user/k8s-configs/backend-deploy.yaml <<'EOF'
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 2
EOF

# Create backend-service.yaml
RUN cat > /home/user/k8s-configs/backend-service.yaml <<'EOF'
---
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  type: ClusterIP
EOF

# Create cache-configmap.yaml
RUN cat > /home/user/k8s-configs/cache-configmap.yaml <<'EOF'
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: cache-config
data:
  config.json: "{}"
EOF

# Create frontend-deploy.yaml
RUN cat > /home/user/k8s-configs/frontend-deploy.yaml <<'EOF'
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 3
EOF

# Create frontend-service.yaml
RUN cat > /home/user/k8s-configs/frontend-service.yaml <<'EOF'
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: LoadBalancer
EOF

# Create redis-service.yaml
RUN cat > /home/user/k8s-configs/redis-service.yaml <<'EOF'
---
apiVersion: v1
kind: Service
metadata:
  name: redis
spec:
  type: ClusterIP
EOF

# Create redis-stateful.yaml
RUN cat > /home/user/k8s-configs/redis-stateful.yaml <<'EOF'
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
spec:
  serviceName: redis
EOF

# Set permissions
RUN chmod 755 /home/user && \
    chmod 755 /home/user/k8s-configs && \
    chmod 644 /home/user/k8s-configs/*.yaml