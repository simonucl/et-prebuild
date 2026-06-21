FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic OS dependencies
# ------------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Python tooling (pytest for the grader)
# ------------------------------------------------------------------
RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial filesystem state expected by the task
# ------------------------------------------------------------------
# Source artefacts
RUN mkdir -p /home/user/mlops/experiments/exp123/logs

RUN cat > /home/user/mlops/experiments/exp123/metrics.json <<'EOF'
{"accuracy": 0.92, "loss": 0.21}
EOF

RUN printf 'DUMMY_MODEL_BINARY_CONTENT\n' \
    > /home/user/mlops/experiments/exp123/model.pkl

RUN cat > /home/user/mlops/experiments/exp123/logs/train.log <<'EOF'
Epoch 1/5 – loss:0.34 – acc:0.78
Epoch 5/5 – loss:0.21 – acc:0.92
EOF

# Destination directory (must start empty)
RUN mkdir -p /home/user/remote_server/exp_artifacts/exp123

# Permissions: allow non-root user to read/write where necessary
RUN chmod -R 0777 /home/user

# ------------------------------------------------------------------
# Environment
# ------------------------------------------------------------------
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# ------------------------------------------------------------------
# Default command
# ------------------------------------------------------------------
CMD ["echo", "Container ready for the MLOps artefact synchronisation task."]