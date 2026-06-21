FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        time \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create user if not exists
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi && \
    mkdir -p /home/user

# Create Kubernetes manifests directory
RUN mkdir -p /home/user/k8s_manifests

# 1. Namespace manifest
RUN cat > /home/user/k8s_manifests/01-namespace.yaml <<'EOF'
---
apiVersion: v1
kind: Namespace
metadata:
  name: test-namespace
EOF

# 2. ConfigMap manifest
RUN cat > /home/user/k8s_manifests/02-configmap.yaml <<'EOF'
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-config
  namespace: test-namespace
data:
  key: value
EOF

# 3. Secret manifest
RUN cat > /home/user/k8s_manifests/03-secret.yaml <<'EOF'
---
apiVersion: v1
kind: Secret
metadata:
  name: test-secret
  namespace: test-namespace
stringData:
  password: s3cr3t
EOF

# 4. Deployment manifest
RUN cat > /home/user/k8s_manifests/04-deployment.yaml <<'EOF'
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-deploy
  namespace: test-namespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test
  template:
    metadata:
      labels:
        app: test
    spec:
      containers:
        - name: nginx
          image: nginx:1.25-alpine
EOF

# 5. Service manifest
RUN cat > /home/user/k8s_manifests/05-service.yaml <<'EOF'
---
apiVersion: v1
kind: Service
metadata:
  name: test-svc
  namespace: test-namespace
spec:
  type: ClusterIP
  selector:
    app: test
  ports:
    - port: 80
      targetPort: 80
EOF

# 6. CRD manifest
RUN cat > /home/user/k8s_manifests/06-crd.yaml <<'EOF'
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: widgets.example.com
spec:
  group: example.com
  names:
    kind: Widget
    plural: widgets
    singular: widget
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
  status:
    acceptedNames: {}
    conditions: []
    storedVersions: []
EOF

# Set permissions on manifest files
RUN chmod 0644 /home/user/k8s_manifests/*.yaml

# Create operator directory and apply script
RUN mkdir -p /home/user/k8s_operator

RUN cat > /home/user/k8s_operator/apply.sh <<'EOF'
#!/usr/bin/env bash
# Simulate "kubectl apply -f ..." by concatenating manifests to /dev/null.
# Exit status is always 0.
cat "$@" > /dev/null
EOF

RUN chmod 0755 /home/user/k8s_operator/apply.sh

# Set ownership
RUN chown -R user:user /home/user && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Default command
CMD echo "Container for Kubernetes manifest benchmarking challenge." && echo "Refer to the task instructions for details on what to do."