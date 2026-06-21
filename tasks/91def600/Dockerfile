FROM ubuntu:22.04

RUN set -e && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/cloud-migration/configs \
             /home/user/cloud-migration/scripts \
             /home/user/cloud-migration/logs

RUN cat > /home/user/cloud-migration/configs/dev-context.yaml <<'EOF'
apiVersion: v1
kind: Config
clusters:
- cluster:
    server: https://dev.k8s.local
  name: dev-cluster
contexts:
- context:
    cluster: dev-cluster
    user: dev-user
  name: dev-context
current-context: dev-context
users:
- name: dev-user
  user:
    token: DEV123TOKEN
EOF

RUN cat > /home/user/cloud-migration/scripts/set-dev-env.sh <<'EOF'
#!/usr/bin/env bash
export K8S_CLUSTER_NAME=dev-cluster
export K8S_NAMESPACE=default
export IMAGE_TAG=v1.0.0
EOF

RUN chmod +x /home/user/cloud-migration/scripts/set-dev-env.sh

RUN cat > /home/user/cloud-migration/Dockerfile <<'EOF'
FROM alpine:3.17
RUN apk add --no-cache python3 py3-pip
COPY . /app
WORKDIR /app
CMD ["python3", "-m", "http.server", "8080"]
EOF

RUN cat > /home/user/cloud-migration/README.md <<'EOF'
# Cloud Migration Dev Environment
This repository provides the minimal scaffolding required to reproduce our
development Kubernetes context locally. It includes:
* kubectl context for the `dev-cluster`
* helper script for environment variables
* lightweight Alpine-based Dockerfile for service prototyping
EOF

RUN { \
        echo "2024-01-01 10:00:00 | mkdir -p /home/user/cloud-migration"; \
        echo "2024-01-01 10:00:01 | mkdir -p /home/user/cloud-migration/configs"; \
        echo "2024-01-01 10:00:02 | mkdir -p /home/user/cloud-migration/scripts"; \
        echo "2024-01-01 10:00:03 | mkdir -p /home/user/cloud-migration/logs"; \
        echo "2024-01-01 10:00:04 | touch /home/user/cloud-migration/configs/dev-context.yaml"; \
    } > /home/user/cloud-migration/logs/setup.log

RUN chmod 755 /home/user

LABEL Author="Cloud-Migration-Scaffold"
LABEL Description="Container pre-configured with cloud-migration developer scaffold and pytest"