FROM ubuntu:22.04

# Labels
LABEL Author="Auto-generated for Kubernetes manifest upgrade task"
LABEL Task="Batch update nginx images to nginx:1.21 using find + xargs"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Base directory
RUN mkdir -p /home/user/manifests/ns1 && \
    mkdir -p /home/user/manifests/ns2 && \
    mkdir -p /home/user/manifests/ns3

# 1. /home/user/manifests/dep_proxy.yaml
RUN cat <<'EOF' > /home/user/manifests/dep_proxy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-proxy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-proxy
  template:
    metadata:
      labels:
        app: nginx-proxy
    spec:
      containers:
      - name: proxy
        image: nginx
        ports:
        - containerPort: 80
EOF

# 2. /home/user/manifests/ns1/dep-nginx.yaml
RUN cat <<'EOF' > /home/user/manifests/ns1/dep-nginx.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 2
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
        image: nginx
        ports:
        - containerPort: 80
EOF

# 3. /home/user/manifests/ns1/svc.yaml
RUN cat <<'EOF' > /home/user/manifests/ns1/svc.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
EOF

# 4. /home/user/manifests/ns2/dep-api.yaml
RUN cat <<'EOF' > /home/user/manifests/ns2/dep-api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: api
        image: myorg/api:latest
        ports:
        - containerPort: 8080
EOF

# 5. /home/user/manifests/ns2/dep-nginx-2.yml
RUN cat <<'EOF' > /home/user/manifests/ns2/dep-nginx-2.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-alt
spec:
  template:
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
EOF

# 6. /home/user/manifests/ns3/job.yaml
RUN cat <<'EOF' > /home/user/manifests/ns3/job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: demo-job
spec:
  template:
    spec:
      containers:
      - name: demo
        image: busybox
        command: ["echo", "Hello"]
      restartPolicy: Never
EOF

# Ensure the agent (non-root at runtime) can read & write everything
RUN chmod -R 777 /home/user/manifests && \
    chmod 755 /home/user