FROM ubuntu:22.04

# Author: FinOps Task Setup
# Description: Container with initial state for FinOps version bump task. Pytest installed.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 755 /home /home/user && \
    mkdir -p /home/user/finops-tool && \
    chmod 755 /home/user/finops-tool

RUN cat >/home/user/finops-tool/version.txt <<'EOF'
2.1.4
EOF

RUN chmod 644 /home/user/finops-tool/version.txt

RUN cat >/home/user/finops-tool/CHANGELOG.md <<'EOF'
# Changelog

## [2.1.4] - 2023-07-15
### Fixed
- Fixed tagging bug in cost explorer sync (#32)

## [2.1.3] - 2023-06-10
### Added
- Added forecast cost anomaly detection (#28)
EOF

RUN chmod 644 /home/user/finops-tool/CHANGELOG.md

ENV HOME=/home/user