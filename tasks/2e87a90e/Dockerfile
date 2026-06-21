FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        make \
        zip \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create project directory structure
RUN mkdir -p /home/user/doc-project/markdown

# intro.md
RUN cat > /home/user/doc-project/markdown/intro.md <<'EOF'
# Introduction

This is the introduction document.

EOF

# setup.md
RUN cat > /home/user/doc-project/markdown/setup.md <<'EOF'
# Setup

Follow these steps to set up the project.

EOF

# Adjust permissions
RUN chmod -R a+rwX /home/user/doc-project && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8