FROM ubuntu:22.04

# Label
LABEL Author="patch-level-bump-sample"

# Update package index and install Python & pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create initial filesystem state for the exercise
RUN mkdir -p /home/user/project

# VERSION file with initial version
RUN printf "1.4.2\n" > /home/user/project/VERSION

# CHANGELOG.md with initial content
RUN cat > /home/user/project/CHANGELOG.md <<'EOF'
# Changelog

All notable changes to this project will be documented in this file.

## [1.4.2] - 2023-08-20
- Fixed security minor bug
EOF

# Ensure write permissions for non-root users who will run inside the container
RUN chmod -R 777 /home/user

# Clean up apt cache to reduce image size
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PYTHONIOENCODING=utf-8

# Default command
CMD ["/bin/bash"]