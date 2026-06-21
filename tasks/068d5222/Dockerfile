FROM ubuntu:22.04

# Labels
LABEL Author="ChatGPT"
LABEL Description="Exercise container for Kubernetes YAML manipulation task"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

RUN mkdir -p /home/user/manifests

RUN cat <<'DEPLOY' > /home/user/manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webserver
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
        image: nginx:1.19
        ports:
        - containerPort: 80
DEPLOY

RUN cat <<'SERVICE' > /home/user/manifests/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: web-svc
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
SERVICE

RUN cat <<'CONFIG' > /home/user/manifests/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: web-config
data:
  index.html: |
    <h1>Hello World!</h1>
CONFIG

RUN chmod 644 /home/user/manifests/*.yaml && \
    chmod 755 /home/user /home/user/manifests && \
    chown -R 1000:1000 /home/user

CMD ["/bin/bash"]