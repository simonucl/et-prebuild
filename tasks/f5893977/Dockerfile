FROM ubuntu:22.04

# Basic tooling
RUN set -eux; \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create application directory structure
RUN mkdir -p /home/user/app

# version.txt with initial version 1.4.2 (newline included)
RUN printf "1.4.2\n" > /home/user/app/version.txt

# Initial CHANGELOG.md
RUN cat > /home/user/app/CHANGELOG.md <<'EOF'
## [1.4.2] - 2023-08-30
### Fixed
- Improved timeout handling for external API requests.

## [1.4.1] - 2023-08-12
### Changed
- Upgraded Alpine base image from 3.17 to 3.18.
EOF

# Ensure non-root users can modify the files during testing
RUN chmod 777 /home/user/app && \
    chmod 666 /home/user/app/version.txt /home/user/app/CHANGELOG.md

# Fix /home/user permissions (from environment section)
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8