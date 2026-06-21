FROM ubuntu:22.04

# Labels
LABEL Author="Automation Task Prep"
LABEL Description="Container primed for curl version logging exercise with pytest pre-installed."

# Help information (as comments):
# This image provides:
#   • A dummy curl package registered at version 7.74.0-1ubuntu2.18.
#   • Pytest installed for automated grading.
#   • A writable /home/user directory where the agent will create curl_version.log.

RUN set -e && \
    echo "Updating apt index and installing prerequisites..." && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip

RUN echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest

RUN echo "Creating writable home directory for the agent..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN echo "Building dummy curl package at required version (7.74.0-1ubuntu2.18)..." && \
    mkdir -p /tmp/curlpkg/DEBIAN

RUN cat > /tmp/curlpkg/DEBIAN/control <<'EOF'
Package: curl
Version: 7.74.0-1ubuntu2.18
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Dummy Builder <builder@example.com>
Description: Placeholder curl package to satisfy testing requirements.
EOF

RUN mkdir -p /tmp/curlpkg/usr/bin && \
    ln -s /bin/true /tmp/curlpkg/usr/bin/curl && \
    chmod 0755 /tmp/curlpkg/usr/bin

RUN dpkg-deb --build /tmp/curlpkg /tmp/curl_7.74.0-1ubuntu2.18_amd64.deb && \
    dpkg -i /tmp/curl_7.74.0-1ubuntu2.18_amd64.deb

RUN echo "Cleaning up build artifacts and apt caches..." && \
    rm -rf /tmp/curlpkg /tmp/curl_7.74.0-1ubuntu2.18_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV HOME=/home/user

WORKDIR /home/user