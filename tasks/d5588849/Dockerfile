FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create experiment directories and files
RUN mkdir -p /home/user/experiments/run_001 && \
    mkdir -p /home/user/experiments/run_002 && \
    printf "run_001 model checkpoint\n" > /home/user/experiments/run_001/model.pkl && \
    printf '{"accuracy": 0.91, "loss": 0.23}\n' > /home/user/experiments/run_001/metrics.json && \
    printf "run_002 model checkpoint\n" > /home/user/experiments/run_002/model.pkl && \
    printf '{"accuracy": 0.93, "loss": 0.19}\n' > /home/user/experiments/run_002/metrics.json

# Create empty writable destination directories
RUN mkdir -p /home/user/backups && \
    mkdir -p /home/user/backup_logs

# Make everything under /home/user writable by any unprivileged user
RUN chmod -R a+rwx /home/user

ENV LC_ALL=C
ENV LANG=C
ENV PYTHONUNBUFFERED=1

WORKDIR /home/user