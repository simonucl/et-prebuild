FROM ubuntu:22.04

# Help section
# Author example@example.com
# Description "Container prepared for Markdown line-length lint task"

RUN set -eu && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/docs

RUN cat > /home/user/docs/introduction.md <<'EOF'
# Introduction to Our Deployment Process

This document describes how to deploy the application.
It covers prerequisites, environment variables, and step-by-step procedures that ensure a smooth rollout to production.
EOF

RUN cat > /home/user/docs/deploy_guide.md <<'EOF'
# Deployment Guide
Make sure you have completed all unit tests, integration tests, and performance benchmarks before proceeding to deployment.
EOF

RUN cat > /home/user/docs/changelog.md <<'EOF'
# Changelog
## [1.0.1] - 2023-04-21
- Fixed bug in authentication.
- Improved latency.
- Added support for distributed tracing which lets the system gracefully handle and visualize end-to-end request flow, even under high load.
EOF

RUN cat > /home/user/docs/README.md <<'EOF'
# Project Documentation
EOF

RUN chmod 0755 /home/user/docs && chmod 0644 /home/user/docs/*.md

ENV PYTHONIOENCODING=utf-8

CMD ["bash"]