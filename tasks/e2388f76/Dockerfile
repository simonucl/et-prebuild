FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/credentials

RUN cat <<'EOF' > /home/user/credentials/settings.yml
aws:
  access_key_id: OLD_ACCESS_KEY
  secret_access_key: OLD_SECRET_KEY
database:
  user: dbuser
  password: verysecret
EOF

RUN cat <<'EOF' > /home/user/credentials/settings.toml
[aws]
access_key_id = "OLD_ACCESS_KEY"
secret_access_key = "OLD_SECRET_KEY"

[database]
user = "dbuser"
password = "verysecret"
EOF

RUN chmod 0644 /home/user/credentials/settings.yml && \
    chmod 0644 /home/user/credentials/settings.toml && \
    chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1