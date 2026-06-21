FROM ubuntu:22.04

# Basic tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Pre-populate filesystem
RUN mkdir -p /home/user/raw_runs/run_42 && \
    mkdir -p /home/user/.metrics_source && \
    mkdir -p /home/user/experiments

RUN : > /home/user/raw_runs/run_42/model.pt
RUN printf '{}\n' > /home/user/raw_runs/run_42/metrics.json

RUN cat > /home/user/.metrics_source/sim_metrics.csv <<'EOF'
23.1,45.2
25.5,46.1
26.3,47.0
24.1,46.5
22.8,45.9
EOF

RUN chmod -R 777 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Labels
LABEL Author="MLOps Task Preparer"
LABEL Version="v1.0"
LABEL Description="Container providing the initial state for the experiment archive & system monitoring task."

CMD echo "Apptainer container ready. Start a shell with:  apptainer exec <container> /bin/bash"