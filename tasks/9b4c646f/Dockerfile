FROM ubuntu:22.04

# Help / runscript info
# Apptainer container for version-bump task.
# Project directory: /home/user/project

ENV PROJECT_DIR=/home/user/project
ENV PATH=$PATH:/home/user/.local/bin

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project

RUN cat <<'EOF' > /home/user/project/package.json
{
  "name": "myapp",
  "version": "1.2.3",
  "description": "Sample app"
}
EOF

RUN cat <<'EOF' > /home/user/project/CHANGELOG.md
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial stub entries.

## [1.2.3] - 2023-08-01
### Added
- Previous stuff.
EOF

RUN chmod -R a+rw /home/user && chmod 755 /home/user