FROM ubuntu:22.04

# Install Python tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Prepare the initial experiment directory tree and log files
RUN mkdir -p /home/user && chmod 755 /home/user

RUN mkdir -p \
    /home/user/experiments/run_alpha/logs \
    /home/user/experiments/run_beta/logs \
    /home/user/experiments/run_gamma/logs

# run_alpha logs
RUN cat > /home/user/experiments/run_alpha/logs/node1.log <<'EOF'
TRAINING_COMPLETE
Epoch 10/10 finished
EOF

RUN cat > /home/user/experiments/run_alpha/logs/node2.log <<'EOF'
Init OK
TRAINING_COMPLETE
EOF

# run_beta logs
RUN cat > /home/user/experiments/run_beta/logs/node1.log <<'EOF'
TRAINING_COMPLETE
All good
EOF

RUN cat > /home/user/experiments/run_beta/logs/node2.log <<'EOF'
ERROR: CUDA out of memory
EOF

# run_gamma logs
RUN cat > /home/user/experiments/run_gamma/logs/node1.log <<'EOF'
Something
TRAINING_COMPLETE
EOF

RUN cat > /home/user/experiments/run_gamma/logs/node2.log <<'EOF'
TRAINING_COMPLETE
Done
EOF

# Set sane permissions (directories 0755, files 0644)
RUN find /home/user/experiments -type d -exec chmod 0755 {} + && \
    find /home/user/experiments -type f -exec chmod 0644 {} +

# Ensure /usr/local binaries and site-packages are visible
ENV PATH="/usr/local/bin:${PATH}"