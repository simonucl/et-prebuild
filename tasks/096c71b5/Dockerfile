FROM ubuntu:22.04

# Labels
LABEL Author="devsecops-task"
LABEL Description="Container for Kubernetes latest image tag scanning assignment"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create non-root user and home
RUN useradd -ms /bin/bash user

# Populate manifests directory
RUN mkdir -p /home/user/manifests

# deployment.yaml
RUN cat <<'EOF' > /home/user/manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 2
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
          image: nginx:latest
          ports:
            - containerPort: 80
EOF

# statefulset.yaml
RUN cat <<'EOF' > /home/user/manifests/statefulset.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cache
spec:
  serviceName: "redis"
  replicas: 1
  selector:
    matchLabels:
      app: cache
  template:
    metadata:
      labels:
        app: cache
    spec:
      containers:
        - name: redis
          image: redis:latest
          ports:
            - containerPort: 6379
EOF

# Fix ownership
RUN chown -R user:user /home/user

# Environment settings
RUN chmod 755 /home/user
ENV PATH=/home/user/.local/bin:$PATH