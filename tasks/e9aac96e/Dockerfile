FROM ubuntu:22.04

# Labels
LABEL Author="Auto-generated for MLOps Experiment Task"
LABEL Description="Provides initial environment with dummy training script and writable experiments directory."

# Environment
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Install required packages and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-venv \
        jq \
        coreutils \
        procps \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create /home/user and experiments directory
RUN mkdir -p /home/user/experiments

# Provide the dummy training script
RUN cat > /home/user/train_dummy.sh <<'EOF'
#!/usr/bin/env bash
# ------------------------------------------------------------
# Dummy training script for the MLOps exercise.
# Produces deterministic start/end markers and some sample lines.
# ------------------------------------------------------------
echo "=== DUMMY TRAINING START ==="
for i in $(seq 1 5); do
    echo "epoch ${i}: loss $(( RANDOM % 100 ))"
    chmod 755 /home/user
    sleep 0.1
done
echo "=== DUMMY TRAINING END ==="
exit 0
EOF

RUN chmod +x /home/user/train_dummy.sh

# Ensure write permissions for non-root users (the student)
RUN chmod -R 0777 /home/user

WORKDIR /home/user