FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial repository structure
RUN mkdir -p /home/user/k8s-operator/deploy

# VERSION file
RUN printf '1.2.3' > /home/user/k8s-operator/VERSION

# operator-deployment.yaml
RUN cat <<'YAML' > /home/user/k8s-operator/deploy/operator-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-operator
spec:
  template:
    spec:
      containers:
      - name: manager
               image: myrepo/myoperator:1.2.3
               imagePullPolicy: IfNotPresent
YAML

# CHANGELOG.md
RUN cat <<'CHANGELOG' > /home/user/k8s-operator/CHANGELOG.md
## [1.2.3] - 2023-05-11

 - Fix CRD validation issue

## [1.2.2] - 2023-03-02

 - Improve reconcilers
 - Bump controller-runtime
CHANGELOG

# Permissions
RUN chmod -R a+rwx /home/user/k8s-operator && \
    chmod a+rwx /home/user && \
    chmod 755 /home/user

ENV PYTHONUNBUFFERED=1