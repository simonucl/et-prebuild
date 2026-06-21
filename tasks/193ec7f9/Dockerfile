FROM ubuntu:22.04

# Help / metadata
# Author: pipeline-patch-exercise
# Description: Base image for Git-Ops ETL patch exercise – provides initial state and pytest.

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/etl/config && \
    mkdir -p /home/user/etl/logs

RUN cat <<'EOF' > /home/user/etl/config/pipeline.yml
version: 1
steps:
  extract:
    source: "s3://raw-data"
  transform:
    script: "transform.py"
  load:
    destination: "warehouse"
EOF

RUN chmod -R 0775 /home/user/etl

RUN chmod 755 /home/user

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin