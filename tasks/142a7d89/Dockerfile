FROM ubuntu:22.04

# Help / labels from %labels section
# Original %labels content:
# chmod 755 /home/user
LABEL Author="Apptainer setup for archive-experiment exercise"

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-setuptools ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/experiments/run_01

RUN cat > /home/user/experiments/run_01/model.bin << 'EOF'
MODEL_WEIGHTS_v1.0
MODEL_WEIGHTS_v1.0
MODEL_WEIGHTS_v1.0
MODEL_WEIGHTS_v1.0
MODEL_WEIGHTS_v1.0
EOF

RUN cat > /home/user/experiments/run_01/metrics.json << 'EOF'
{
  "accuracy": 0.93,
  "loss": 0.2
}
EOF

RUN cat > /home/user/experiments/run_01/config.yaml << 'EOF'
learning_rate: 0.001
epochs: 10
EOF

RUN chmod 0777 /home/user && \
    chmod 644 /home/user/experiments/run_01/*