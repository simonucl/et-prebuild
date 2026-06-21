FROM ubuntu:22.04

# Help section
# Container for the 'Audit & Correct YAML/TOML Configuration' task.
# You can start an interactive shell with:  apptainer exec <image> /bin/bash

LABEL Author="dev-team"
LABEL Description="Container providing initial state for the YAML/TOML compliance task."
LABEL Maintainer="you@example.com"

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/compliance/service_a && \
    mkdir -p /home/user/compliance/service_b

RUN cat <<'YAML_EOF' > /home/user/compliance/service_a/config.yaml
apiVersion: v1
service:
  enabled: false
  port: 8080
logging:
  level: INFO
YAML_EOF

RUN cat <<'TOML_EOF' > /home/user/compliance/service_b/settings.toml
[server]
active = false
listen_ip = "0.0.0.0"
listen_port = 9000

[security]
ciphers = ["TLS_AES_128_GCM_SHA256"]
TOML_EOF

RUN chmod -R 777 /home/user/compliance && chmod 755 /home/user