FROM ubuntu:22.04

# Author: ExampleAuthor
# Description: Initial filesystem and tooling for “Bring MegaCRM back online” exercise.

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/app/config && \
    mkdir -p /home/user/app/certs

RUN cat <<'EOF' > /home/user/app/config/settings.yml
app:
  name: MegaCRM
  version: "2.3.0"
maintenance_mode: false
limits:
  max_users: 500
  max_connections: 80
EOF

RUN cat <<'EOF' > /home/user/app/config/database.toml
[database]
engine = "postgresql"
host = "localhost"
port = 5432
name = "megacrm"
user = "legacy_user"
password = "changeme"
EOF

RUN touch /home/user/app/certs/db-client.pem

RUN chmod -R a+rwx /home/user

RUN chmod 755 /home/user

ENV PATH=$PATH:/usr/local/bin

CMD ["/bin/bash"]