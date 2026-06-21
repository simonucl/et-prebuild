# syntax=docker/dockerfile:1
# From the local SIF image; Docker cannot use .sif, so we use the equivalent Ubuntu base
FROM ubuntu:22.04

# Post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data_pipeline && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/data_pipeline

RUN cat >/home/user/data_pipeline/update.sh <<'EOF'
#!/usr/bin/env bash
if [[ "$1" == "--force" ]]; then
    echo "Applying forced update …"
    echo "Update applied successfully."
    exit 0
else
    echo "Attempting dry-run update …"
    echo "DRY-RUN FAILED – manual confirmation required" >&2
    exit 1
fi
EOF

RUN chmod 0755 /home/user/data_pipeline/update.sh

# Environment section
ENV PATH="/usr/bin:${PATH}"

RUN chmod 755 /home/user

# Labels section
LABEL Author="example"
LABEL Description="Environment for Data-Mule deployment task with pytest installed"

# Run script
CMD ["bash"]