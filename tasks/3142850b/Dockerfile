FROM ubuntu:22.04

# Update package index and install Python + pip
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-distutils \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Prepare filesystem layout
RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/finops_data/dev && \
    mkdir -p /home/user/finops_data/prod && \
    mkdir -p /home/user/finops_data/staging

# Generate sample files with exact byte sizes
RUN dd if=/dev/zero bs=1 count=4321  of=/home/user/finops_data/dev/tmp.log     2>/dev/null && \
    dd if=/dev/zero bs=1 count=12345 of=/home/user/finops_data/prod/data1.bin  2>/dev/null && \
    dd if=/dev/zero bs=1 count=6789  of=/home/user/finops_data/staging/readme.txt 2>/dev/null

# Set permissions
RUN chmod -R a+rX /home/user/finops_data

# Labels
LABEL Author="FinOps Container Builder"
LABEL Description="Environment for FinOps disk-usage snapshot exercise. Pytest pre-populated."

CMD echo "Container built for the FinOps disk-usage snapshot exercise." && \
    echo "Run your commands inside the container to complete the task."