FROM ubuntu:22.04

# Labels
LABEL Author="On-Call Security Engineer Prep"
LABEL Description="Base image prepared for credential rotation & dependency refresh task"
LABEL Maintainer="AI Assistant"

# Update package index and install Python with pip
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    ln -sf /usr/bin/pip3 /usr/local/bin/pip && \
    pip3 install --no-cache-dir pytest

# Create /home/user/microservice with legacy credentials
RUN mkdir -p /home/user/microservice && \
    printf 'API_KEY=oldkey123\nAPI_SECRET=oldsecret456\n' > /home/user/microservice/.env && \
    chmod -R a+rwx /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Default entrypoint
ENTRYPOINT ["/bin/bash", "-c", "chmod 755 /home/user && exec \"$@\"", "--"]