FROM ubuntu:22.04

# Author DevOpsChallenge
# Description "Container prepared for Kubernetes manifest synchronisation task; includes pytest and pre-populated remote_repo."

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/remote_repo && \
    chmod 755 /home/user && \
    chmod 755 /home/user/remote_repo

RUN cat > /home/user/remote_repo/nginx-deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
EOF

RUN cat > /home/user/remote_repo/nginx-service.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
EOF

RUN chmod 644 /home/user/remote_repo/nginx-deployment.yaml /home/user/remote_repo/nginx-service.yaml

RUN rm -rf /home/user/k8s-manifests || true && \
    rm -f /home/user/sync.log || true