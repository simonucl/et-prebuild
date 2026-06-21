# Author="Auto-generated for Markdown clean-up task"
# Description="Container pre-seeded with draft Markdown files and pytest installed"
# Help:
# This Apptainer image provides the initial state for the Markdown
# clean-up exercise. It contains:
#   • /home/user/docs/drafts/{intro,setup,usage}.md
#   • pytest pre-installed for the autograder.

FROM ubuntu:22.04

RUN set -e && apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    ca-certificates \
    tzdata && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/docs/drafts && \
    chmod 777 /home/user && \
    chmod 777 /home/user/docs && \
    chmod 777 /home/user/docs/drafts

RUN cat > /home/user/docs/drafts/intro.md <<'EOF'
# Introduction
This project aims to demonstrate simple text-processing techniques.

TODO: Add background
More to come. TBD
EOF

RUN cat > /home/user/docs/drafts/setup.md <<'EOF'
# Setup
Follow these steps to prepare the environment.

TODO: Describe installation
Configuration TBD
EOF

RUN cat > /home/user/docs/drafts/usage.md <<'EOF'
# Usage
Here we'll cover usage scenarios.

TODO: Provide examples
Edge cases TBD
Another TODO: finalize images
EOF

RUN chmod 666 /home/user/docs/drafts/*.md && chmod 755 /home/user

ENV HOME=/home/user