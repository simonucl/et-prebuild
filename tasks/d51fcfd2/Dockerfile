FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Ensure the /home/user hierarchy exists
RUN mkdir -p /home/user/projects/clean-sensor-data

# 1. VERSION file with initial version 0.2.1
RUN printf "0.2.1\n" > /home/user/projects/clean-sensor-data/VERSION

# 2. CHANGELOG.md with historical entries (no 0.2.2 yet)
RUN cat > /home/user/projects/clean-sensor-data/CHANGELOG.md <<'EOF'
# Changelog

## [0.2.1] - 2024-04-10
### Fixed
- Ensure correct parsing of humidity values (#17)

## [0.2.0] - 2024-03-01
### Added
- Initial public release
EOF

# 3. Permissions: make sure future (non-root) processes can edit files
RUN chmod -R a+rwX /home/user

ENV HOME=/home/user

WORKDIR /home/user