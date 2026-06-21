# Author: Apptainer setup for version-bump task
# Help:
# This Apptainer image provides the initial filesystem state for the
# “project-docs” version-bump exercise and includes pytest for automated grading.

FROM ubuntu:22.04

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && chmod 755 /home/user

RUN mkdir -p /home/user/project-docs && \
    printf "1.4.2\n" > /home/user/project-docs/VERSION

RUN cat <<'EOF' > /home/user/project-docs/CHANGELOG.md
# Changelog

All notable changes to this project will be documented in this file following Keep a Changelog principles.

## [1.4.2] - 2024-01-10
### Changed
- Tweaked API docs.
EOF

RUN chmod -R u+rwX,go+rX /home/user/project-docs