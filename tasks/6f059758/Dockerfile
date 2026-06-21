FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial filesystem state for the exercise
# ------------------------------------------------------------------
RUN mkdir -p /home/user/project/config

# site_config.yaml — development (initial) version
RUN cat > /home/user/project/config/site_config.yaml <<'EOF'
site_name: "My Portfolio"
production: false
assets:
  js_minify: false
  css_minify: false
EOF

# database.toml — development (initial) version
RUN cat > /home/user/project/config/database.toml <<'EOF'
[database]
host = "localhost"
port = 5432
user = "admin"
password = "admin"
pool_size = 5
EOF

# Ensure correct permissions (read-only for files, readable dirs)
RUN chmod 755 /home/user && \
    chmod -R 755 /home/user/project && \
    chmod 644 /home/user/project/config/site_config.yaml && \
    chmod 644 /home/user/project/config/database.toml

# DO NOT create /home/user/update_logs — it must be absent initially

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8