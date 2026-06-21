FROM ubuntu:22.04

# Base dependencies
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates \
        python3-setuptools && \
    pip3 install --no-cache-dir pytest

# Prepare the initial exercise filesystem layout
# Ensure /home/user exists and is writable by any unprivileged runtime user.
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Create the artifacts directory structure.
RUN mkdir -p /home/user/artifacts/bin && \
    chmod 0755 /home/user/artifacts && \
    chmod 0755 /home/user/artifacts/bin

# Create the required files.
RUN touch /home/user/artifacts/bin/cliapp && \
    touch /home/user/artifacts/bin/libhelper.so && \
    printf 'Demo artifact set\n' > /home/user/artifacts/README.md

# Set the correct permissions.
RUN chmod 0644 /home/user/artifacts/bin/cliapp && \
    chmod 0644 /home/user/artifacts/bin/libhelper.so && \
    chmod 0644 /home/user/artifacts/README.md && \
    chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /home/user

ENTRYPOINT []
CMD ["/bin/bash"]