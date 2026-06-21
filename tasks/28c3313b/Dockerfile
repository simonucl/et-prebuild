FROM ubuntu:22.04

# Author: container-builder
# Description: Environment for log filtering task with pytest installed.
# This container provides:
#   - /home/user/datasets/raw_records.log with required content
#   - pytest installed
#   - No /home/user/clean_data directory

LABEL Author="container-builder" \
      Description="Environment for log filtering task with pytest installed."

ENV HOME=/home/user

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/datasets

RUN cat > /home/user/datasets/raw_records.log <<'EOF'
ABC123 SUCCESS Data loaded
DEF456 FAILURE Data missing
XYZ789 SUCCESS Completed
abc111 SUCCESS lowercase
123ABC SUCCESS misplaced
LMN000 SUCCESS component
NOP999 FAULT unexpected
QRS321 SUCCESS processed
TUV654 DEFER waiting
GHI777 SUCCESS final
EOF

RUN chmod 755 /home/user && \
    chmod 755 /home/user/datasets && \
    chmod 644 /home/user/datasets/raw_records.log