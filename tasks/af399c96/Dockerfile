# syntax=docker/dockerfile:1
FROM ubuntu:22.04

LABEL Author="Kubernetes-Manifest-Prep"
LABEL Description="Container that provides the pre-conversion state of Kubernetes manifests encoded in ISO-8859-1 with CRLF endings. Pytest is installed for task validation."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN if ! id -u user >/dev/null 2>&1; then useradd -m -u 1000 -s /bin/bash user; fi

RUN install -d -m 0755 /home/user/k8s/manifests

RUN printf 'apiVersion: extensions/v1beta1\r\nkind: Deployment\r\nmetadata:\r\n  name: my-app\r\nspec:\r\n  replicas: 2\r\n  template:\r\n    metadata:\r\n      labels:\r\n        app: my-app\r\n    spec:\r\n      containers:\r\n      - name: my-app\r\n        image: nginx:1.19\r\n' \
    > /home/user/k8s/manifests/deployment.yaml

RUN printf 'apiVersion: v1\r\nkind: Service\r\nmetadata:\r\n  name: my-app-service\r\nspec:\r\n  selector:\r\n    app: my-app\r\n  ports:\r\n    - port: 80\r\n      targetPort: 80\r\n' \
    > /home/user/k8s/manifests/service.yaml

RUN printf 'apiVersion: networking.k8s.io/v1\r\nkind: Ingress\r\nmetadata:\r\n  name: my-app-ingress\r\nspec:\r\n  rules:\r\n    - host: myapp.example.com\r\n      http:\r\n        paths:\r\n          - path: /\r\n            pathType: Prefix\r\n            backend:\r\n              service:\r\n                name: my-app-service\r\n                port:\r\n                  number: 80\r\n' \
    > /home/user/k8s/manifests/ingress.yaml

RUN chown -R 1000:1000 /home/user && \
    chmod 0644 /home/user/k8s/manifests/*.yaml && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"

CMD echo "Container for Kubernetes manifest conversion task." && echo "You can now run pytest to execute the provided tests."