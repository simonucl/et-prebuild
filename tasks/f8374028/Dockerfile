FROM ubuntu:22.04

# Help:
# This container provides the initial filesystem and software (Python + pytest)
# needed for the Markdown heading aggregation exercise.

ENV HOME=/home/user

RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/docs/source

RUN cat >/home/user/docs/source/intro.md <<'EOF'
# Introduction
This project contains example Markdown documentation.

Some more prose that is irrelevant for this task.
EOF

RUN cat >/home/user/docs/source/setup.md <<'EOF'
# Setup
Follow these steps to prepare your environment.

# Installation
Run the installation script after cloning the repository.
EOF

RUN cat >/home/user/docs/source/usage.md <<'EOF'
# Usage
After installation, you can run the program as follows:
EOF

RUN cat >/home/user/docs/source/duplicateHeading.md <<'EOF'
# Introduction
This is a duplicate heading introduced on purpose.
EOF

RUN chmod -R a+r /home/user/docs/source && \
    find /home/user/docs/source -type d -exec chmod a+rx {} +

RUN chmod 755 /home/user

LABEL Author="example@example.com"
LABEL Description="Environment for Markdown heading aggregation task."