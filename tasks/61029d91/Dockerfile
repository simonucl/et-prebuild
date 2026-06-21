# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install Python, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#############
# Task setup
#############

# Create required directory structure
RUN mkdir -p /home/user/app/config

# Create settings.yaml with the exact initial content
RUN cat > /home/user/app/config/settings.yaml <<'EOF'
---
server:
  host: "0.0.0.0"
  port: 8080
debug: false
---
EOF

# Ensure an empty changes.log file exists
RUN : > /home/user/app/config/changes.log

# Set permissions so the unprivileged agent can modify the files
RUN chmod 777 /home/user/app /home/user/app/config && \
    chmod 666 /home/user/app/config/settings.yaml /home/user/app/config/changes.log

# Ensure home directory permissions as in runscript
RUN chmod 755 /home/user

# Default command
CMD ["/bin/bash"]