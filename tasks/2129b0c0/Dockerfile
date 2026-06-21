# Author: performance-engineering-task
# Description: Container with pre-existing application drops for symbolic-link profiling exercise
# Help:
# This container provides the initial state for the profiling-workspace task.
# It pre-installs pytest for automated grading and places two mock application
# drops under /home/user/apps/ ready for students to work with.

FROM ubuntu:22.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -e; \
    echo "Updating package lists and installing Python tooling..."; \
    apt-get update -qq; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        bash \
        coreutils; \
    pip3 install --no-cache-dir pytest; \
    echo "Creating initial filesystem layout under /home/user..."; \
    mkdir -p /home/user/apps/appAlpha-1.2/bin; \
    mkdir -p /home/user/apps/appAlpha-1.2/perfdata; \
    mkdir -p /home/user/apps/appBeta-2.0/bin; \
    mkdir -p /home/user/apps/appBeta-2.0/perfdata; \
    chmod 755 /home/user; \
    find /home/user/apps -type d -exec chmod 755 {} \;

RUN cat <<'EOF' >/home/user/apps/appAlpha-1.2/bin/alpha
#!/bin/bash
echo "Alpha v1.2"
EOF

RUN cat <<'EOF' >/home/user/apps/appBeta-2.0/bin/beta
#!/bin/bash
echo "Beta v2.0"
EOF

RUN chmod 755 /home/user/apps/appAlpha-1.2/bin/alpha && \
    chmod 755 /home/user/apps/appBeta-2.0/bin/beta