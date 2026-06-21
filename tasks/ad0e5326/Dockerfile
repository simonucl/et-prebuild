# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help and labels
LABEL Author="task-preparer"
LABEL Description="Container providing the initial state for the Markdown publication staging task."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/work_in_progress

RUN cat > /home/user/work_in_progress/overview.md <<'EOF'
# Project Overview
This document provides an overview of the project.
TODO: expand details.
EOF

RUN cat > /home/user/work_in_progress/install.md <<'EOF'
# Installation Guide
Follow these steps to install the application.
Step 1: ...
TODO: add screenshots.
EOF

RUN cat > /home/user/work_in_progress/faq.md <<'EOF'
# FAQ
Frequently asked questions will go here.
EOF

RUN chmod -R a+rwX /home/user

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && rm -rf /var/lib/apt/lists/*