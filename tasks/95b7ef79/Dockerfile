FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Set up directory structure
RUN mkdir -p /home/user/projects/pipeline

# Create pipeline.yaml
RUN cat <<'EOF' > /home/user/projects/pipeline/pipeline.yaml
version: 1
stages:
  - build
  - test
jobs:
  build_app:
    stage: build
    script:
      - echo "Building Android app"
  run_tests:
    stage: test
    script:
      - echo "Running unit tests"
EOF

# Create config.toml
RUN cat <<'EOF' > /home/user/projects/pipeline/config.toml
[build]
android_sdk = "/opt/android/sdk"
ios_sdk     = "/Applications/Xcode.app"

[release]
version_code = 42
track        = "beta"
EOF

# Permissions
RUN chmod -R a+rwx /home/user/projects
RUN chmod 755 /home/user

# Labels
LABEL Author="pipeline-setup"
LABEL Purpose="Initial state for CI/CD maintenance task"