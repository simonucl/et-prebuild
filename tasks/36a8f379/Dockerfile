FROM ubuntu:22.04

# Install required OS packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/manifests && \
    chmod -R 0777 /home/user

# frontend-deploy.json
RUN cat > /home/user/manifests/frontend-deploy.json <<'EOF_FRONTEND'
{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "frontend",
    "namespace": "prod",
    "labels": {
      "app": "frontend"
    }
  },
  "spec": {
    "replicas": 3,
    "template": {
      "metadata": {
        "labels": {
          "app": "frontend"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "frontend",
            "image": "company/frontend:v2"
          }
        ]
      }
    }
  }
}
EOF_FRONTEND

# backend-deploy.json
RUN cat > /home/user/manifests/backend-deploy.json <<'EOF_BACKEND'
{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "backend",
    "namespace": "prod",
    "labels": {
      "app": "backend"
    }
  },
  "spec": {
    "replicas": 2,
    "template": {
      "metadata": {
        "labels": {
          "app": "backend"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "backend",
            "image": "company/backend:v1"
          }
        ]
      }
    }
  }
}
EOF_BACKEND

# worker-deploy.json
RUN cat > /home/user/manifests/worker-deploy.json <<'EOF_WORKER'
{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "worker",
    "namespace": "batch",
    "labels": {
      "app": "worker"
    }
  },
  "spec": {
    "replicas": 4,
    "template": {
      "metadata": {
        "labels": {
          "app": "worker"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "worker",
            "image": "company/worker:v5"
          }
        ]
      }
    }
  }
}
EOF_WORKER

# Set permissions
RUN chmod 0644 /home/user/manifests/*.json && \
    chmod 755 /home/user

# Environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Labels
LABEL Author="Kubernetes-Platform-Operator-Setup"
LABEL Description="Container with initial state for manifest summarization task"
LABEL Version="v1"