# syntax=docker/dockerfile:1
# Author: task-generator
# Description: Initial workstation state for the compliance audit task.
# Help:
# This container sets up the initial, non-compliant configuration files that
# the agent must bring into compliance during testing.

FROM ubuntu:22.04

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip ca-certificates tzdata && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/user -s /bin/bash user

RUN CONFIG_DIR=/home/user/configs && \
    mkdir -p "${CONFIG_DIR}"

RUN CONFIG_DIR=/home/user/configs && \
    cat <<'EOF' > "${CONFIG_DIR}/app_config.yml"
database:
  host: 127.0.0.1
  port: 5432
  user: appuser
  password: changeme
logging:
  level: info
  file: /var/log/app.log
EOF

RUN CONFIG_DIR=/home/user/configs && \
    cat <<'EOF' > "${CONFIG_DIR}/app_settings.toml"
[server]
address = "0.0.0.0"
port = 8080

[feature_flags]
enable_beta = false
use_cache = true
EOF

RUN chown -R user:user /home/user && \
    chmod 755 /home/user /home/user/configs && \
    chmod 664 /home/user/configs/app_config.yml /home/user/configs/app_settings.toml

CMD ["/bin/bash"]