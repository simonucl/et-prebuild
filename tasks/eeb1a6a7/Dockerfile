FROM ubuntu:22.04

LABEL Author="MLOps-Exercise-Builder"
LABEL Description="Base image that provides the initial filesystem state and tooling for the experiment registration task."

# --- System packages ----------------------------------------------------
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# --- Python tooling ------------------------------------------------------
RUN pip3 install --no-cache-dir pytest

# --- Directory hierarchy -------------------------------------------------
RUN mkdir -p /home/user/mlops/configs && \
    mkdir -p /home/user/mlops/registry && \
    mkdir -p /home/user/mlops/logs

# --- Initial YAML file ---------------------------------------------------
RUN cat > /home/user/mlops/configs/experiments.yaml <<'EOF'
experiments:
  - id: 1
    name: baseline_cnn
    dataset: mnist
    accuracy: 0.975
    artifact_uri: s3://ml-bucket/experiments/1
  - id: 2
    name: mobilenet_v2
    dataset: cifar10
    accuracy: 0.855
    artifact_uri: s3://ml-bucket/experiments/2
EOF

# --- Initial TOML file ---------------------------------------------------
RUN cat > /home/user/mlops/registry/artifacts.toml <<'EOF'
# MLOps experiment artifact registry
[baseline_cnn]
uri = "s3://ml-bucket/experiments/1"

[mobilenet_v2]
uri = "s3://ml-bucket/experiments/2"
EOF

# --- Permissions ---------------------------------------------------------
RUN chmod -R a+rw /home/user/mlops && \
    chmod 755 /home/user

CMD ["/bin/bash"]