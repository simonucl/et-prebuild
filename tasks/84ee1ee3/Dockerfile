# Using ubuntu:22.04 as the closest equivalent to the local SIF image
FROM ubuntu:22.04

# -----------------------------------------------------------------
# Base OS packages and Python tooling
# -----------------------------------------------------------------
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest

# -----------------------------------------------------------------
# Create directory structure for the exercise
# -----------------------------------------------------------------
RUN mkdir -p /home/user/cluster_logs && \
    mkdir -p /home/user/policies && \
    mkdir -p /home/user/reports

# -----------------------------------------------------------------
# Kubernetes kubelet log snapshots
# -----------------------------------------------------------------
RUN cat <<'EOF' > /home/user/cluster_logs/node-alpha.log
2024-06-06T08:15:42Z kubelet[987]: Started pod: auth-5d9c8d7cdf-abcde (cpu_limit=250m)
2024-06-06T08:16:10Z kubelet[987]: Started pod: billing-6c8dcbf9f-xyz12 (cpu_limit=none)
2024-06-06T08:16:35Z kubelet[987]: Started pod: payments-7f9d7c9d7f-q2g7x (cpu_limit=250m)
EOF

RUN cat <<'EOF' > /home/user/cluster_logs/node-bravo.log
2024-06-06T08:20:11Z kubelet[123]: Started pod: cart-7c9d7c9d7f-mnopq (cpu_limit=none)
2024-06-06T08:21:11Z kubelet[123]: Started pod: search-6c8dcbf9f-rstuv (cpu_limit=250m)
EOF

RUN cat <<'EOF' > /home/user/cluster_logs/node-charlie.log
2024-06-06T08:25:07Z kubelet[456]: Started pod: catalogue-5d9c8d7cdf-wxyz1 (cpu_limit=250m)
EOF

# -----------------------------------------------------------------
# Initial Deployment YAML (without resources section)
# -----------------------------------------------------------------
RUN cat <<'EOF' > /home/user/policies/secured-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: insecure-service
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: insecure-service
    spec:
      containers:
      - name: insecure-container
        image: nginx:latest
EOF

# -----------------------------------------------------------------
# Ensure correct permissions
# -----------------------------------------------------------------
RUN chmod -R a+rw /home/user

# -----------------------------------------------------------------
# Environment variables
# -----------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# The chmod from %environment must be executed at build time
RUN chmod 755 /home/user