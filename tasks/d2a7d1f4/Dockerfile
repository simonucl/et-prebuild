FROM ubuntu:22.04

# Update package lists and install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gnupg \
        ca-certificates \
        coreutils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the evaluation framework
RUN pip3 install --no-cache-dir pytest

# Create the directory structure
RUN mkdir -p /home/user/experiments/run_15

# Create metrics.json with the required contents (ending with a newline)
RUN cat > /home/user/experiments/run_15/metrics.json <<'EOF'
{
  "accuracy": 0.953,
  "loss": 0.127
}
EOF

# Ensure there is exactly one trailing newline
RUN echo >> /home/user/experiments/run_15/metrics.json

# Set permissions as mandated by the tests
RUN chmod 0700 /home/user/experiments/run_15 && \
    chmod 0600 /home/user/experiments/run_15/metrics.json

# Give ownership to the typical non-root user (UID 1000 / GID 1000)
RUN chown -R 1000:1000 /home/user

# Set default command
CMD ["bash", "-c", "chmod 755 /home/user && echo 'Container for GPG encryption task. Run your commands inside an interactive shell.' && exec /bin/bash"]