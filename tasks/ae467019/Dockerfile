# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author etl_task_preparer
# Description "Environment for ETL configuration task with pytest pre-installed."
# Original runscript:
#   echo "Container built for ETL config task."
#   echo "Use this container to complete the exercise."

ENV PYTHONUNBUFFERED=1

RUN chmod 755 /home/user || true

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/etl_pipeline/config && \
    mkdir -p /home/user/etl_pipeline/logs

RUN cat > /home/user/etl_pipeline/config/config.yaml <<'YAML'
source:
  type: #TODO
  host: #TODO
  port: #TODO
  database: #TODO
  user: #TODO
  password: #TODO

transformations: []

destination:
  type: #TODO
  path: #TODO
YAML

RUN cat > /home/user/etl_pipeline/config/pipeline.toml <<'TOML'
[default]
timezone = "UTC"
retry = 3
TOML

RUN chmod -R a+rw /home/user/etl_pipeline