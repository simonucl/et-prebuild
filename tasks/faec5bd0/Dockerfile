# Author: Apptainer build script
# Description: Container for data-cleaning exercise. Provides initial CSV data and pytest for testing.
# Help:
# This container sets up the initial state for the data-cleaning exercise.
# Directories and files are created under /home/user/webdev as required,
# and pytest is installed for automated testing.

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        gawk \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/webdev/data && \
    mkdir -p /home/user/webdev/output

RUN cat > /home/user/webdev/data/products.csv <<'EOF'
id,name,price,status
1,Widget,19.99,active
2,Gadget,29.49,discontinued
3,Doohickey,9.95,active
4,Thingamajig,4.50,discontinued
5,Whatsit,14.00,active
EOF

RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/webdev && \
    chmod 0755 /home/user/webdev/data && \
    chmod 0777 /home/user/webdev/output && \
    chmod 0644 /home/user/webdev/data/products.csv

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user