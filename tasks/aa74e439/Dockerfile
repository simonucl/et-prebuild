# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author ChatGPT
# Description: Environment for Kubernetes Operator log-filtering exercise with pytest pre-installed.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/k8s-operator/logs && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/k8s-operator && \
    chmod 0777 /home/user/k8s-operator/logs

RUN cat <<'EOF' > /home/user/k8s-operator/logs/operator.log
2023-08-01T08:30:12Z level=info    msg="Starting controller"
2023-08-01T08:30:13Z level=error   code=CM001 ns=default name=app-config   msg="Missing ConfigMap"
2023-08-01T08:30:14Z level=warning msg="Retry reconcile"
2023-08-01T08:30:15Z level=error   code=SV001 ns=prod    name=web-svc      msg="Service not found"
2023-08-01T08:30:16Z level=info    msg="Reconcile complete"
2023-08-01T08:30:17Z level=error   code=DEP404 ns=staging name=api-deployment msg="Deployment failed"
2023-08-01T08:31:18Z level=info    msg="Starting controller"
2023-08-01T08:31:19Z level=error   code=CM001 ns=default name=app-config   msg="Missing ConfigMap"
2023-08-01T08:31:20Z level=warning msg="Retry reconcile"
2023-08-01T08:31:21Z level=error   code=SV001 ns=prod    name=web-svc      msg="Service not found"
EOF

RUN chmod 0644 /home/user/k8s-operator/logs/operator.log && \
    chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

LABEL Author="ChatGPT"
LABEL Description="Environment for Kubernetes Operator log-filtering exercise with pytest pre-installed."