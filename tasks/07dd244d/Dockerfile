FROM ubuntu:22.04

# Basic development tools
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create directory structure
RUN mkdir -p /home/user/docs/raw

# installation.md
RUN cat <<'EOF' > /home/user/docs/raw/installation.md
# Installation
To install the **AwesomeApp**, follow these steps:
1. Download the package. [TODO] 
2. Run the installer.
It will guide you through the setup.  
EOF

# usage.md
RUN cat <<'EOF' > /home/user/docs/raw/usage.md
# Usage Guide
After installation, you can start AwesomeApp via terminal:
$ awesomeapp start
For advanced options, consult the manual. [TODO]  
EOF

# changelog.md
RUN cat <<'EOF' > /home/user/docs/raw/changelog.md
# Changelog
## v1.0.1
- Fixed minor bugs.  
## v1.0.0
- Initial release. [TODO]
EOF

# Make /home/user writable
RUN chmod -R a+rwX /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8