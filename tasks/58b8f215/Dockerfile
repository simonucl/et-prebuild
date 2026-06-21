# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Basic OS packages + Python tooling for the automated pytest suite
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Create the required directory structure
# ------------------------------------------------------------------
RUN mkdir -p /home/user/qa_envs/base \
    /home/user/qa_envs/overrides \
    /home/user/qa_envs/generated

# -------- base/app_config.yml --------
RUN cat > /home/user/qa_envs/base/app_config.yml <<'EOF'
app:
  name: DemoApp
  version: "1.0.0"
  debug: false
database:
  host: localhost
  port: 5432
  username: demo
  password: demo123
EOF

# -------- overrides/dev.yml --------
RUN cat > /home/user/qa_envs/overrides/dev.yml <<'EOF'
app:
  version: "1.1.0"
  debug: true
database:
  host: dev-db.internal
  port: 5433
  username: dev_user
  password: dev_pass
features:
  experimental: true
  logging: verbose
EOF

# -------- overrides/test.yml --------
RUN cat > /home/user/qa_envs/overrides/test.yml <<'EOF'
app:
  version: "1.1.0"
database:
  host: test-db.internal
  port: 5434
  username: test_user
  password: test_pass
features:
  experimental: false
  logging: normal
EOF

# -------- settings.toml --------
RUN cat > /home/user/qa_envs/settings.toml <<'EOF'
[build]
threads = 8
optimize = true

[qa]
environment = "multi"
EOF

# ------------------------------------------------------------------
# Permissions
# ------------------------------------------------------------------
RUN chmod -R a+rwX /home/user/qa_envs && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Metadata (from %labels)
# ------------------------------------------------------------------
LABEL Author="QA-Container-Generator" \
      Description="Initial environment for QA configuration merging task" \
      Version="1.0"