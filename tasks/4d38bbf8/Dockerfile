# Converted from Apptainer definition file
FROM ubuntu:22.04

# Help text
# This container image sets up the initial filesystem for the deterministic
# backup exercise and provides pytest for the accompanying test suite.

LABEL Author="container-prep-script"
LABEL Description="Deterministic backup exercise – initial state with pytest installed."

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tar \
        gzip \
        coreutils && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/important_data/config && \
    mkdir -p /home/user/important_data/projectA && \
    mkdir -p /home/user/important_data/projectB/figures

RUN cat <<'EOF' > /home/user/important_data/config/settings.conf
---
# Application settings
mode = production
timeout = 30
---
EOF

RUN cat <<'EOF' > /home/user/important_data/projectA/data.csv
id,value
1,42
2,97
EOF

RUN echo "Project A quarterly report — draft" > /home/user/important_data/projectA/report.txt

RUN dd if=/dev/urandom of=/home/user/important_data/projectB/presentation.pptx bs=1 count=16 status=none && \
    dd if=/dev/urandom of=/home/user/important_data/projectB/figures/diagram.png bs=1 count=16 status=none

RUN chmod -R a+rX /home/user && \
    chmod u+w /home/user

# Permissions from %environment that require execution
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C
ENV LANG=C