# Converted from Apptainer definition
FROM ubuntu:22.04

# Help / metadata
LABEL Author="documentation-setup"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create documentation workspace
RUN mkdir -p /home/user/docs

RUN cat >/home/user/docs/intro.md <<'EOF'
# Introduction
Placeholder text.
EOF

RUN cat >/home/user/docs/usage.md <<'EOF'
# Usage Guide
Placeholder text.
EOF

RUN cat >/home/user/docs/faq.md <<'EOF'
# FAQ
Placeholder text.
EOF

# Permissions
RUN chmod 777 /home/user/docs
RUN chmod 755 /home/user

# Environment variables
ENV PYTHONIOENCODING="utf-8"