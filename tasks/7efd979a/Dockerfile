FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare the microservice repository
RUN mkdir -p /home/user/microservice

# version.txt
RUN cat > /home/user/microservice/version.txt <<'EOF'
1.2.4
EOF

# CHANGELOG.md
RUN cat > /home/user/microservice/CHANGELOG.md <<'EOF'
# Changelog

## [1.2.4] - 2023-01-15
### Added
- Initial release.
EOF

# Permissions
RUN chmod -R a+rwX /home/user/microservice && \
    chmod -R a+rwX /home/user && \
    chmod 755 /home/user

ENV PYTHONUNBUFFERED=1