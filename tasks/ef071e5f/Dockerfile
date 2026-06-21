FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest

# Prepare the /home/user directory
RUN mkdir -p /home/user && chmod 0777 /home/user

# Apply environment-time permissions change from %environment
RUN chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# No runscript equivalent needed; default Docker behavior execs CMD/ENTRYPOINT