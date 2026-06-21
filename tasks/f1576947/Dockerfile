FROM ubuntu:22.04

# Container image for the “Kubernetes manifest backup” exercise.
# Provides the initial filesystem state expected by the test-suite and
# includes pytest for verification.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/k8s/manifests && \
    mkdir -p /home/user/backup/archives

RUN cat > /home/user/k8s/manifests/deployment.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 2
EOF

RUN cat > /home/user/k8s/manifests/service.yaml <<'EOF'
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  type: ClusterIP
EOF

RUN cat > /home/user/k8s/manifests/configmap.yaml <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  key: value
EOF

RUN touch /home/user/backup/backup.log && \
    chmod -R a+rX /home/user/k8s && \
    chmod 0777 /home/user/backup && \
    chmod 0777 /home/user/backup/archives && \
    chmod 0666 /home/user/backup/backup.log

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8