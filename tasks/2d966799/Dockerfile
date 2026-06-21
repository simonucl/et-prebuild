FROM ubuntu:22.04

# Labels
LABEL Author="KubernetesInventoryTask"
LABEL Description="Environment for Kubernetes manifest inventory exercise"

# Update and install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the autograder
RUN python3 -m pip install --no-cache-dir --upgrade pip setuptools && \
    python3 -m pip install --no-cache-dir pytest

# Create initial filesystem layout expected by the tests
RUN mkdir -p /home/user/k8s/manifests

# deployment-web.yaml
RUN cat >/home/user/k8s/manifests/deployment-web.yaml <<'EOF'
# filename:deployment-web.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-frontend
spec:
  replicas: 3
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
EOF

# deployment-api.yaml
RUN cat >/home/user/k8s/manifests/deployment-api.yaml <<'EOF'
# filename:deployment-api.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: server
        image: my-api:2.0
EOF

# statefulset-db.yaml
RUN cat >/home/user/k8s/manifests/statefulset-db.yaml <<'EOF'
# filename:statefulset-db.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db-storage
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: db
    spec:
      containers:
      - name: postgres
        image: postgres:13
EOF

# Ensure every manifest ends with a single trailing newline
RUN for f in /home/user/k8s/manifests/*.yaml; do \
        sed -n '$p' "$f" | grep -q '^$' || echo >>"$f"; \
    done

# Permissions: allow the (non-root) runner to read manifests and
# create new directories/files under /home/user/k8s
RUN chmod -R a+rwX /home/user/k8s && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Container for the Kubernetes inventory task. Use this container to run the exercise tests or your own commands."]