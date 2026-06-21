# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest for the grader
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest tomli && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Set up the initial working directory and seed files for the exercise
# ------------------------------------------------------------------
RUN mkdir -p /home/user/deploy

# config.yaml (version 1.2.3, no release_date yet)
RUN cat > /home/user/deploy/config.yaml <<'EOF'
app_name: "WeatherApp"
version: "1.2.3"
environment: "staging"
maintainers:
  - "alice"
  - "bob"
EOF

# metadata.toml (version 1.2.3, no release_date yet)
RUN cat > /home/user/deploy/metadata.toml <<'EOF'
[package]
name = "weather_app"
version = "1.2.3"

[build]
target = "x86_64"
EOF

# Make sure the runtime (non-root) user can modify everything
RUN chmod -R 777 /home/user/deploy

# Runtime environment setup
RUN chmod 755 /home/user
ENV PATH="/home/user/.local/bin:${PATH}"

LABEL Author="Exercise Preparation Bot" \
      Description="Container image for release-manager version bump exercise (pytest included)."