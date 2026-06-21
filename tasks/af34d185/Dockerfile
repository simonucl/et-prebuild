# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / runscript information
# Container for the 'artifact summary' task.
# The initial inventory is located at /home/user/repos/artifacts/inventory.csv
# Create /home/user/logs/artifact_summary.log as specified to complete the task.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/repos/artifacts && \
    chmod 0755 /home/user/repos && \
    chmod 0755 /home/user/repos/artifacts

RUN cat <<'EOF' > /home/user/repos/artifacts/inventory.csv
filename,size_bytes
core-1.2.3.jar,2048
utils-4.5.6.jar,4096
plugin-0.9.1.zip,1024
readme.txt,512
cli-2.0.0.tar.gz,3072
EOF

RUN chmod 0644 /home/user/repos/artifacts/inventory.csv && \
    rm -rf /home/user/logs

RUN chmod 755 /home/user