FROM ubuntu:22.04

LABEL Author="MLOps-Setup"
LABEL Description="Environment for version-bump single-command task"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/experiments && \
    echo "1.4.2" > /home/user/experiments/VERSION

RUN cat > /home/user/experiments/CHANGELOG.md <<'EOF'
# Changelog
## [1.4.2] - 2023-08-22
### Fixed
- Resolved metrics logging race condition.

## [1.4.1] - 2023-08-15
### Added
- Introduced early stopping callback.
EOF

RUN chmod -R a+rwX /home/user/experiments && chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

CMD ["bash"]