# Author your_name
# Version v1.0
# Description Container for Kubernetes manifest patching task. Provides initial manifests and pytest for automated grading.

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    echo "Updating apt repositories and installing Python tooling..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl \
        gnupg && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating initial directory structure and manifest files..." && \
    mkdir -p /home/user/k8s-manifests && \
    chmod 755 /home/user && \
    chmod 755 /home/user/k8s-manifests

RUN cat <<'EOF' > /home/user/k8s-manifests/deployment-app.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: mycorp/app:0.9
          ports:
            - containerPort: 8080
EOF

RUN cat <<'EOF' > /home/user/k8s-manifests/service-app.yml
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  type: ClusterIP
  selector:
    app: app
  ports:
    - port: 80
      targetPort: 8080
EOF

RUN cat <<'EOF' > /home/user/k8s-manifests/configmap-app.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
EOF

RUN chmod 644 /home/user/k8s-manifests/*.yml

CMD echo "This container is set up for the Kubernetes manifest patching task." && echo "Navigate to /home/user/k8s-manifests to begin."