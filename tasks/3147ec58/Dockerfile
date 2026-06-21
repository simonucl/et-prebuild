FROM ubuntu:22.04

# Author: Example
# Description: Environment setup for the artifact-archiving task

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/experiments/run_01 && \
    mkdir -p /home/user/archives

RUN cat >/home/user/experiments/run_01/metrics.json <<'EOF'
{
  "accuracy": 0.94,
  "loss": 0.23
}
EOF

RUN echo 'MODEL_WEIGHTS' > /home/user/experiments/run_01/model.bin

RUN cat >/home/user/experiments/run_01/logs.txt <<'EOF'
Training started...
Training completed successfully.
EOF

RUN chmod -R a+rX /home/user && \
    chmod -R a+w /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8