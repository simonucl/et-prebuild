FROM ubuntu:22.04

# Author build-task-generator
# Description "Environment for nightly-build digest extraction task"

ENV PYTHONUNBUFFERED=1

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/builds

RUN cat > /home/user/builds/artifact_manifest.csv <<'EOF'
build_id,artifact_name,version,checksum
101,core-lib,1.0.0,2873acb
102,ui-assets,1.0.1,9fbc211
103,service-bin,2.0.0,17ab899
EOF

RUN chmod -R a+rw /home/user/builds && \
    chmod 755 /home/user