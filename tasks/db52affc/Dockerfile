FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Prepare initial repository state for the capacity-planner project
RUN mkdir -p /home/user/projects/capacity-planner

# VERSION file with initial content
RUN printf '1.3.4\n' > /home/user/projects/capacity-planner/VERSION

# CHANGELOG.md with initial content (must exactly match expected text)
RUN cat > /home/user/projects/capacity-planner/CHANGELOG.md <<'EOF'
# Changelog

## [1.3.4] - 2023-03-20
### Added
- Initial support for CPU burst predictions.
EOF

# Ensure the unprivileged runtime user can modify the repository
RUN chmod -R 777 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/bin/sh", "-c", "exec \"$@\"", "--"]