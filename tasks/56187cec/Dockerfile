# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Install Python and pytest
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Prepare initial project state expected by the automated tests
# ------------------------------------------------------------------
RUN mkdir -p /home/user/project

# config.yaml (initial state with maintenance set to false)
RUN cat > /home/user/project/config.yaml <<'EOF'
server:
  host: "0.0.0.0"
  port: 8080
feature_flags:
  maintenance: false
  beta: true
EOF

# settings.toml (initial state with maintenance set to false)
RUN cat > /home/user/project/settings.toml <<'EOF'
[database]
host = "localhost"
port = 5432
user = "webapp"
maintenance = false
EOF

# Ensure the student can modify these files/directories later
RUN chmod 777 /home/user/project && \
    chmod 666 /home/user/project/config.yaml /home/user/project/settings.toml && \
    chmod 755 /home/user

# ------------------------------------------------------------------
# Environment settings
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# ------------------------------------------------------------------
# Default action is to drop into a shell
# ------------------------------------------------------------------
CMD ["/bin/bash"]