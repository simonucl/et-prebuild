# Help / Labels
# Author: AI-generated definition file
# Description: Sets up the pristine initial state for the configuration-patching task and installs pytest.

FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/app/config && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/app && \
    chmod 0777 /home/user/app/config

RUN cat >/home/user/app/config/settings.yaml <<'EOF'
service:
  enabled: false
  version: "1.4.3"
  port: 8080
logging:
  level: "DEBUG"
  format: "text"
EOF

RUN cat >/home/user/app/config/database.toml <<'EOF'
[database]
name = "test_db"
user = "dev"
password = "devpass"
host = "localhost"
port = 5432
pool_size = 5
EOF

RUN chmod 0644 /home/user/app/config/settings.yaml /home/user/app/config/database.toml && \
    chmod -R a+rX /home/user && \
    chown -R 1000:1000 /home/user || true

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8