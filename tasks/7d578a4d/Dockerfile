FROM ubuntu:22.04

# Help text
# This container sets up the initial file system state for the observability
# configuration challenge. Two configuration files live in
# /home/user/observability with their original values, and pytest is
# installed so the autograder can verify the initial state.

LABEL Author="Apptainer Task Preparer"
LABEL Description="Container providing initial state for observability configuration task."

ENV PATH="/usr/local/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN groupadd -g 1000 user || true && \
    useradd -m -u 1000 -g 1000 user || true

RUN mkdir -p /home/user/observability

RUN cat <<'YAML' > /home/user/observability/watchers.yaml
alerts:
  cpu_usage:
    enabled: true
    threshold: 85
  memory_usage:
    enabled: true
    threshold: 90
YAML

RUN cat <<'TOML' > /home/user/observability/grafana.toml
[auth]
disable_login_form = false

[users]
allow_sign_up  = true
default_theme  = "light"
TOML

RUN chown -R 1000:1000 /home/user

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user