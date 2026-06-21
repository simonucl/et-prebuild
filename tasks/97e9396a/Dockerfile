FROM ubuntu:22.04

# Install Python tooling and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir pytest

# Create a non-privileged user
RUN useradd -m -s /bin/bash user

# Set up initial directory structure
RUN mkdir -p /home/user/mlops/experiments/exp42 && \
    mkdir -p /home/user/mlops/logs && \
    mkdir -p /home/user/remote_store

# Populate the experiment artifacts
RUN printf 'DUMMY MODEL DATA\n' > /home/user/mlops/experiments/exp42/model.pkl
RUN cat <<'EOF' > /home/user/mlops/experiments/exp42/metrics.json
{
  "accuracy": 0.93,
  "loss": 0.12
}
EOF

# Ensure the regular user can read/write everything under /home/user
RUN chown -R user:user /home/user && \
    chmod -R u+rwX,go+rX /home/user

# Apply environment-time chmod specified in %environment
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/home/user/.local/bin:${PATH}"