FROM ubuntu:22.04

# Help section as comments
# Container image for the "dataset sync" exercise.
# Provides the initial folder structure and files for the task and includes
# Python with pytest plus rsync for the student's solution.

# Install system packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        rsync \
        ca-certificates \
        curl \
        gnupg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the evaluation harness
RUN pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/workspace/datasets && \
    mkdir -p /home/user/remote_share/datasets

# Create sample1.csv
RUN cat >/home/user/workspace/datasets/sample1.csv <<'EOF'
id,value
1,10
2,20
EOF

# Create sample2.csv
RUN cat >/home/user/workspace/datasets/sample2.csv <<'EOF'
id,value
3,30
4,40
EOF

# Create sample3.csv
RUN cat >/home/user/workspace/datasets/sample3.csv <<'EOF'
id,value
5,50
6,60
EOF

# Remote (simulated server) copies - Only sample1.csv and sample3.csv exist remotely at start
RUN cp /home/user/workspace/datasets/sample1.csv /home/user/remote_share/datasets/sample1.csv && \
    cp /home/user/workspace/datasets/sample3.csv /home/user/remote_share/datasets/sample3.csv

# Ensure non-root users can write to the working directories
RUN chmod -R a+rwX /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8