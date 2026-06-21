# Converted from Apptainer definition file
FROM ubuntu:22.04

# Basic development tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        csvtool && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python packages
RUN pip3 install --no-cache-dir pytest

# Prepare workspace
RUN mkdir -p /home/user && chmod 0777 /home/user
RUN mkdir -p /home/user/experiments && chmod 0777 /home/user/experiments

RUN cat <<'EOF' > /home/user/experiments/metrics.csv
run_id,accuracy,loss
run_001,0.87,0.34
run_002,0.91,0.29
run_003,0.89,0.31
EOF

RUN chmod 0666 /home/user/experiments/metrics.csv

# Environment setup
RUN chmod 755 /home/user
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin