# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Post section
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/release/config && \
    mkdir -p /home/user/release/static && \
    mkdir -p /home/user/release/tmp

RUN cat > /home/user/release/app.py <<'EOF'
# Application entry
def main():
    pass  # TODO Update database credentials
EOF

RUN chmod 0644 /home/user/release/app.py

RUN echo "# sample settings" > /home/user/release/config/settings.conf && \
    chmod 0600 /home/user/release/config/settings.conf

RUN echo "PNG" > /home/user/release/static/logo.png && \
    chmod 0666 /home/user/release/static/logo.png

RUN echo "TODO remove debug statements before production" > /home/user/release/tmp/debug.log && \
    chmod 0777 /home/user/release/tmp/debug.log

RUN mkdir -p /home/user/security_scans && \
    chmod 0755 /home/user/security_scans

# Environment section
RUN chmod 755 /home/user
ENV PATH="/usr/bin:$PATH"

# Labels
LABEL Author="Apptainer Task Setup"
LABEL Description="Environment for security scan exercise with pytest pre-installed."