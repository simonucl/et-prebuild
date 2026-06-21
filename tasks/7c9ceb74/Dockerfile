FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare filesystem
RUN mkdir -p /home/user/db_configs && \
    chmod 777 /home/user/db_configs

# db_settings.yaml
RUN cat > /home/user/db_configs/db_settings.yaml <<'YAML_EOF'
database:
  host: localhost
  port: 5432
  pool:
    size: 10
    timeout: 300

queries:
  optimizer:
    enable: false
    cost_threshold: 100
YAML_EOF

# replication.toml
RUN cat > /home/user/db_configs/replication.toml <<'TOML_EOF'
[replication]
enabled = false
max_replicas = 2

[maintenance]
vacuum = "daily"
TOML_EOF

RUN chmod 666 /home/user/db_configs/db_settings.yaml /home/user/db_configs/replication.toml && \
    chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

LABEL Author="On-Call DB Admin Task Setup"
LABEL Description="Container with initial configuration files and pytest installed for the learner."