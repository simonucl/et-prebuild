# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels
LABEL Author="example"
LABEL Description="Container with initial CI configuration for buildozer task."

# Update apt and install Python plus pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN --mount=type=cache,target=/root/.cache/pip python3 -m pip install --no-cache-dir pytest==7.1.2

# Create the initial state required by the exercise
RUN mkdir -p /home/user/ci

# Initial contents of /home/user/ci/pipeline.yml
RUN cat <<'EOF' > /home/user/ci/pipeline.yml
version: 1
python_packages:
  - pytest==7.1.2
EOF

# Ensure the learner (non-root) can modify the repo
RUN chmod -R a+rwX /home/user/ci

# Ensure home directory permissions
RUN chmod 755 /home/user

# Environment variables from %environment
ENV HOME=/home/user
ENV PATH="/home/user/.local/bin:/usr/local/bin:/usr/bin:/bin"

# %help
# This container sets up the initial state for the buildozer dependency task.

# %runscript equivalent
CMD echo "This container sets up the initial state for the buildozer dependency task."