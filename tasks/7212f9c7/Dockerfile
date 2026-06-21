# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Install Python and pytest
# ------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Prepare initial filesystem state expected by the grader
# ------------------------------------------------------------
RUN mkdir -p /home/user/experiments/exp_alpha && \
    mkdir -p /home/user/experiments/exp_beta && \
    mkdir -p /home/user/experiments/exp_gamma

RUN cat > /home/user/experiments/exp_alpha/config.ini <<'EOF'
[metadata]
experiment_name=exp_alpha
timestamp=2023-08-23T15:34:12Z

[training]
learning_rate=0.001
batch_size=32

[results]
accuracy=0.88
EOF

RUN cat > /home/user/experiments/exp_beta/config.ini <<'EOF'
[metadata]
experiment_name=exp_beta
timestamp=2023-08-24T09:18:45Z

[training]
learning_rate=0.0005
batch_size=64

[results]
accuracy=0.93
EOF

RUN cat > /home/user/experiments/exp_gamma/config.ini <<'EOF'
[metadata]
experiment_name=exp_gamma
timestamp=2023-08-24T17:02:01Z

[training]
learning_rate=0.002
batch_size=32

[results]
accuracy=0.89
EOF

# Allow any non-root user to create new files/directories under /home/user
RUN chmod 0777 /home/user && \
    chmod -R a+rX /home/user/experiments && \
    chmod 755 /home/user

# ------------------------------------------------------------
# Environment settings
# ------------------------------------------------------------
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# ------------------------------------------------------------
# Apptainer runscript equivalent
# ------------------------------------------------------------
# Apptainer image for the experiment-report task. Run your own script inside.