# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: pipeline-task-prep
# Description: Environment for CI/CD validation task with jq and pytest pre-installed

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        jq \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/pipelines

RUN cat > /home/user/pipelines/build-info.json <<'EOF'
{
  "build_id": "1024",
  "commit_sha": "9fceb02d131adf4d4f5aebd3233c2b5da4b8c4c6",
  "artifact_url": "https://ci.example.com/artifacts/1024/app.tar.gz",
  "status": "success"
}
EOF

RUN echo "Placeholder README for CI/CD pipelines workspace." > /home/user/pipelines/README.txt

RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/pipelines && \
    chmod 644 /home/user/pipelines/build-info.json /home/user/pipelines/README.txt && \
    chown -R 1000:1000 /home/user || true

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH=$PATH:/usr/local/bin

# Container runscript equivalent
CMD echo "Container for CI/CD build-info validation task."