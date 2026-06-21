FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Ensure the target user exists (UID/GID 1000 is the common default)
RUN if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user || true; \
        useradd -m -u 1000 -g 1000 user || true; \
    fi

# Create the required directory structure and initial configuration files
RUN mkdir -p /home/user/app/config

RUN cat > /home/user/app/config/settings.yml <<'EOF'
database:
  user: admin
  password: OldPass123
aws:
  access_key: OLDACCESSKEY
  secret_key: OLDSECRETKEY
  region: us-east-1
EOF

RUN cat > /home/user/app/config/credentials.toml <<'EOF'
[default]
username = "admin"
password = "OldPass123"
token    = "OLDTOKEN987"
EOF

# Set required permissions
RUN chmod 0644 /home/user/app/config/settings.yml /home/user/app/config/credentials.toml && \
    chown -R user:user /home/user

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin