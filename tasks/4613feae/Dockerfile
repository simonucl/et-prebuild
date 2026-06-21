FROM ubuntu:22.04

# Help text from %help
# This Apptainer image provides the initial environment for the “track_experiments”
# assignment. Two sample experiment runs are placed under
#   /home/user/mlops/experiments/
# ready for the student-written script to process. The container also includes
# Python, pip, pytest, and jq.

# 1. Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Create non-root user `user`
RUN groupadd -g 1000 user && \
    useradd -m -u 1000 -g 1000 -s /bin/bash user

# 3. Prepare initial filesystem and files
RUN mkdir -p /home/user/mlops/experiments/run_001 && \
    mkdir -p /home/user/mlops/experiments/run_002 && \
    printf '{"lr":0.001,"batch_size":32,"optimizer":"adam"}' > /home/user/mlops/experiments/run_001/config.json && \
    printf '{"accuracy":0.92,"loss":0.35}' > /home/user/mlops/experiments/run_001/metrics.json && \
    printf '{"lr":0.0005,"batch_size":16,"optimizer":"sgd"}' > /home/user/mlops/experiments/run_002/config.json && \
    printf '{"accuracy":0.88,"loss":0.42}' > /home/user/mlops/experiments/run_002/metrics.json && \
    chown -R 1000:1000 /home/user && \
    chmod -R 755 /home/user/mlops

# 4. Python tooling
RUN python3 -m pip install --no-cache-dir pytest

# From %environment — chmod is a command so placed in RUN
RUN chmod 755 /home/user
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

# %runscript note
# MLOps tracking task container. Start a shell manually; no ENTRYPOINT defined.

LABEL Author="someone" \
      Description="Base image for MLOps tracking task with initial experiment data and pytest installed."