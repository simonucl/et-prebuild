FROM ubuntu:22.04

# Help / labels
LABEL Author="task-prep-script"
LABEL Description="Container image that sets up the initial state for the alpha_app migration exercise."

# Install Python tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/downloads/alpha_assets && \
    mkdir -p /home/user/dev && \
    chmod -R 777 /home/user && \
    touch /home/user/downloads/alpha_assets/app.py && \
    touch /home/user/downloads/alpha_assets/helpers.py && \
    touch /home/user/downloads/alpha_assets/test_app.py && \
    touch /home/user/downloads/alpha_assets/test_helpers.py && \
    touch /home/user/downloads/alpha_assets/overview.md && \
    touch /home/user/downloads/alpha_assets/CHANGELOG.md && \
    touch /home/user/downloads/alpha_assets/Dockerfile && \
    touch /home/user/downloads/alpha_assets/LICENSE

# Environment settings
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"