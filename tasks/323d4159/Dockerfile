FROM ubuntu:22.04

# Help / labels from %labels
LABEL Author="ChatGPT"
LABEL Description="Base image for the Kubernetes Operator – Concurrent Apply Benchmark & Manifest Metrics task."

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/manifests

RUN cat << 'EOF' > /home/user/manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 2
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.19
          ports:
            - containerPort: 80
EOF

RUN cat << 'EOF' > /home/user/manifests/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: ClusterIP
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
EOF

RUN cat << 'EOF' > /home/user/manifests/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: example-config
data:
  key1: value1
  key2: value2
EOF

RUN chmod -R 755 /home/user

CMD ["/bin/bash"]