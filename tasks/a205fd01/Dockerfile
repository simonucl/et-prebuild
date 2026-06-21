FROM ubuntu:22.04

# Help / metadata from %help and %labels
LABEL Author="Apptainer Task Prep Bot"
LABEL Description="Environment for Kubernetes manifest disk-usage report task"

RUN set -e && \
    apt-get update -qq && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip install --no-cache-dir pytest && \
    mkdir -p /home/user/k8s-manifests && \
    cd /home/user/k8s-manifests && \
    printf 'apiVersion: v1\nkind: Pod\n' > deployment.yaml && \
    printf 'apiVersion: v1\nkind: Service\n' > service.yaml && \
    printf 'apiVersion: v1\nkind: ConfigMap\n' > configmap.yaml && \
    chmod -R a+rwX /home/user/k8s-manifests && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV LC_ALL=C
ENV LANG=C

CMD ["/bin/bash"]