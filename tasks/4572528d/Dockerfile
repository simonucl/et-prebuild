FROM ubuntu:22.04

# Labels from %labels
LABEL Author="performance-sre"
LABEL Purpose="Deterministic Kubernetes operator benchmark starter image"

# Basic tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Directory structure
RUN mkdir -p /home/user/k8s_operator/manifests && \
    mkdir -p /home/user/benchmark_scripts

# deployment.yaml
RUN cat <<'EOF' > /home/user/k8s_operator/manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-deployment
spec: {}
EOF

# service.yaml
RUN cat <<'EOF' > /home/user/k8s_operator/manifests/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: demo-service
spec: {}
EOF

# configmap.yaml
RUN cat <<'EOF' > /home/user/k8s_operator/manifests/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: demo-config
data: {}
EOF

# apply_manifest.sh
RUN cat <<'EOF' > /home/user/benchmark_scripts/apply_manifest.sh
#!/usr/bin/env bash
# Very small deterministic harness for the benchmarking exercise.
case "$(basename "$1")" in
  deployment.yaml)
    echo "Applied deployment.yaml in 12ms"
    ;;
  service.yaml)
    echo "Applied service.yaml in 8ms"
    ;;
  configmap.yaml)
    echo "Applied configmap.yaml in 5ms"
    ;;
  *)
    echo "Unknown manifest" >&2
    exit 1
    ;;
esac
EOF

RUN chmod 0755 /home/user/benchmark_scripts/apply_manifest.sh

# Permissions for /home/user
RUN chmod -R a+rwX /home/user && chmod 755 /home/user

# No environment variables required
ENV PATH="$PATH"