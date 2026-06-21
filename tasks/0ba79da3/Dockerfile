FROM ubuntu:22.04

# Basic tooling
RUN apt-get update -qq && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates
RUN pip3 install --no-cache-dir pytest

# Prepare directories
RUN mkdir -p /home/user/manifests && mkdir -p /home/user/backups

# deployment.yaml
RUN cat >/home/user/manifests/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: nginx
        image: nginx:1.25
        ports:
        - containerPort: 80
EOF

# service.yaml
RUN cat >/home/user/manifests/service.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: webapp-svc
spec:
  selector:
    app: webapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
EOF

# ingress.yaml
RUN cat >/home/user/manifests/ingress.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-ingress
spec:
  rules:
  - host: webapp.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: webapp-svc
            port:
              number: 80
EOF

# Permissions
RUN chmod -R a+rwX /home/user

# Environment
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Labels
LABEL Author="Apptainer Build Script"
LABEL Description="Container image for the Kubernetes manifests backup exercise. Includes pytest and the initial filesystem state."