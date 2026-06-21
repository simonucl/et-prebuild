# Help: converted from Apptainer definition

FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/experiments/exp_alpha && \
    mkdir -p /home/user/experiments/exp_beta && \
    mkdir -p /home/user/experiments/exp_gamma

RUN cat <<'EOF' > /home/user/experiments/exp_alpha/metrics.csv
epoch,accuracy,loss
1,0.8071,0.6722
2,0.8983,0.3399
3,0.9234,0.1123
EOF

RUN cat <<'EOF' > /home/user/experiments/exp_alpha/config.yaml
model: resnet18
learning_rate: 0.001
epochs: 3
EOF

RUN cat <<'EOF' > /home/user/experiments/exp_beta/metrics.csv
epoch,accuracy,loss
1,0.7550,0.7109
2,0.8662,0.4012
3,0.9111,0.1278
EOF

RUN cat <<'EOF' > /home/user/experiments/exp_beta/config.yaml
model: mobilenetv2
optimizer: adam
learning_rate: 0.0005
epochs: 3
EOF

RUN cat <<'EOF' > /home/user/experiments/exp_gamma/metrics.csv
epoch,accuracy,loss
1,0.8744,0.5080
2,0.9327,0.2414
3,0.9570,0.0931
EOF

RUN cat <<'EOF' > /home/user/experiments/exp_gamma/config.yaml
model: efficientnet_b0
epochs: 3
learning_rate: 0.002
EOF

RUN chmod -R a+rX /home/user && chmod 755 /home/user