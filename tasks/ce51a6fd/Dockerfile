FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Generator"
LABEL Description="Container with pre-populated experiment INI files and pytest installed for student exercises."

#------------------------------------------------------------------
# Basic OS packages
#------------------------------------------------------------------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata \
        bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#------------------------------------------------------------------
# Python tooling for the grader / student
#------------------------------------------------------------------
RUN pip3 install --no-cache-dir pytest

#------------------------------------------------------------------
# Create non-privileged user 'user'
#------------------------------------------------------------------
RUN useradd -m -s /bin/bash user

#------------------------------------------------------------------
# Pre-populate the experiment directories and INI files
#------------------------------------------------------------------
RUN mkdir -p /home/user/experiments/exp001 && \
    mkdir -p /home/user/experiments/exp002 && \
    mkdir -p /home/user/experiments/exp003

# ----- exp001 -----
RUN cat > /home/user/experiments/exp001/config.ini <<'EOF'
[metadata]
experiment_id = exp001
owner = alice
created = 2023-08-10

[dataset]
name = imagenet
version = 1.2

[model]
architecture = resnet50
param_count = 25557032
EOF

# ----- exp002 -----
RUN cat > /home/user/experiments/exp002/config.ini <<'EOF'
[metadata]
experiment_id = exp002
owner = bob
created = 2023-08-11

[dataset]
name = cifar10
version = 3.0

[model]
architecture = mobilenet_v2
param_count = 3504875
EOF

# ----- exp003 -----
RUN cat > /home/user/experiments/exp003/config.ini <<'EOF'
[metadata]
experiment_id = exp003
owner = carol
created = 2023-08-12

[dataset]
name = mnist
version = 1.0

[model]
architecture = lenet
param_count = 60000
EOF

#------------------------------------------------------------------
# Permissions: make sure the non-root user can access everything
#------------------------------------------------------------------
RUN chown -R user:user /home/user && \
    chmod 755 /home/user

ENV PATH="/home/user/.local/bin:$PATH"

USER user
WORKDIR /home/user