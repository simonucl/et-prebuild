FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial project filesystem
RUN mkdir -p /home/user/projects/capacity-planner/data && \
    mkdir -p /home/user/projects/capacity-planner/release_notes

# VERSION file (initial state)
RUN echo "1.4.2" > /home/user/projects/capacity-planner/VERSION

# CHANGELOG.md with previous entry only
RUN cat > /home/user/projects/capacity-planner/CHANGELOG.md <<'EOF'
# Changelog

## [1.4.2] - 2023-08-10
### Fixed
- Patched forecasting overflow bug.
EOF

# usage.log with provided ground-truth data
RUN cat > /home/user/projects/capacity-planner/data/usage.log <<'EOF'
2023-08-01T00:00:00Z,45.2,60.1
2023-08-01T01:00:00Z,55.8,72.3
2023-08-01T02:00:00Z,88.1,95.4
2023-08-01T03:00:00Z,36.4,50.2
2023-08-01T04:00:00Z,50.0,65.0
2023-08-01T05:00:00Z,70.0,80.0
EOF

# Ensure non-root users can read/write everything under /home/user
RUN chmod -R a+rwX /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /home/user

CMD ["echo", "Docker image for the 'capacity-planner' task. No default execution action is defined."]