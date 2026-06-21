FROM ubuntu:22.04

# Labels
LABEL Author="Container preparation for capacity-planner task"

# Environment variables
ENV PATH="/usr/local/bin:$PATH"

# Basic tooling
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata \
        locales && \
    pip3 install --no-cache-dir pytest

# Create initial repository layout for "capacity-planner"
RUN mkdir -p /home/user/capacity-planner/logs

WORKDIR /home/user/capacity-planner

# VERSION file
RUN printf '1.4.3\n' > VERSION

# CHANGELOG with some previous content
RUN cat > CHANGELOG.md <<'EOF'
## [1.4.3] - 2023-09-15

### Fixed
- Resolved memory leak in forecasting engine.
EOF

# Web logs
RUN cat > logs/web.csv <<'EOF'
timestamp,cpu_percent,mem_mb
00:00,12,100
00:01,20,110
00:02,18,95
EOF

# DB logs
RUN cat > logs/db.csv <<'EOF'
timestamp,cpu_percent,mem_mb
00:00,30,210
00:01,45,220
00:02,40,215
EOF

# Initialise Git repository with an initial commit
RUN git init -q && \
    git config user.email "builder@example.com" && \
    git config user.name "Builder" && \
    git add . && \
    git commit -q -m "chore: initial commit 1.4.3"

# Ensure write permissions for non-root users
RUN chmod -R a+rwX /home/user

WORKDIR /home/user

CMD ["/bin/bash"]