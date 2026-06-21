FROM ubuntu:22.04

ENV LC_ALL=C
ENV LANG=C

# Basic tooling: Python + pip + pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial experiment-tracking workspace
RUN mkdir -p /home/user/experiments && \
    chmod 777 /home/user && \
    chmod 777 /home/user/experiments

# experiment_metrics.csv
RUN cat >/home/user/experiments/experiment_metrics.csv <<'EOF'
experiment_id,accuracy,loss
1,0.85,0.45
2,0.88,0.40
EOF
RUN chmod 666 /home/user/experiments/experiment_metrics.csv

# last_run_config.json
RUN printf '{"lr":0.001,"accuracy":0.93,"loss":0.35}' \
    >/home/user/experiments/last_run_config.json && \
    chmod 666 /home/user/experiments/last_run_config.json

# Ensure output files do NOT exist yet
RUN rm -f /home/user/experiments/best_accuracy.json \
          /home/user/experiments/update_log.txt

# Labels
LABEL Author="Container setup for experiment-tracking task"