# Derived from local image ./ubuntu_22.04.sif
FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create working directory structure
RUN mkdir -p /home/user/manifests

# Populate initial deployment.yaml
RUN cat <<'EOF' > /home/user/manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-operator
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: operator
        image: ghcr.io/org/example-operator:1.2.3
EOF

# Populate initial CHANGELOG.md
RUN cat <<'EOF' > /home/user/CHANGELOG.md
# Changelog

All notable changes to this project will be documented in this file.

## [1.2.3] - 2024-05-01
### Added
- Initial release of example-operator
EOF

# Ensure writable permissions for non-root agent
RUN chmod -R 0777 /home/user

# Environment setup
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"