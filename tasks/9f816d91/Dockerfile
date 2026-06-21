FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/manifests

RUN cat > /home/user/manifests/deployment-frontend.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  template:
    spec:
      containers:
      - name: web
        image: myrepo/frontend:v1.0.0
EOF

RUN cat > /home/user/manifests/deployment-backend.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  template:
    spec:
      containers:
      - name: api
        image: myrepo/backend:v1.0.0
EOF

RUN cat > /home/user/manifests/statefulset-db.yaml <<'EOF'
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: db
spec:
  template:
    spec:
      containers:
      - name: postgres
        image: otherrepo/postgres:13
EOF

RUN cat > /home/user/manifests/configmap.yaml <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: example-config
data:
  key1: value1
  key2: value2
EOF

RUN chmod -R a+rwX /home/user && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8