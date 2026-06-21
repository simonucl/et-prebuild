# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author="Automated setup"
# Description="Environment for ML data-prep task with pytest pre-installed"
# This container provides the starting state for the ML data-preparation task.
# Raw CSV files are placed in /home/user/data/raw; no output artefacts have
# been generated yet. Utilities installed include:
#   - python3 + pytest
#   - pigz
#   - GNU parallel

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        pigz \
        parallel \
        ca-certificates \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/data/raw

RUN cat <<'EOF' > /home/user/data/raw/file1.csv
id,name,status,value
1,Alice,train,0.5
2,Bob,test,0.8
3,Carol,train,0.3
4,Dan,train,0.9
EOF

RUN cat <<'EOF' > /home/user/data/raw/file2.csv
id,name,status,value
3,Carol,train,0.3
4,Dan,train,0.9
5,Eve,train,0.4
6,Frank,val,0.7
EOF

RUN chmod 777 /home/user && \
    chmod 777 /home/user/data && \
    chmod 644 /home/user/data/raw/file1.csv /home/user/data/raw/file2.csv

RUN mkdir -p /home/user/.parallel && \
    touch /home/user/.parallel/will-cite && \
    chmod 600 /home/user/.parallel/will-cite

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH