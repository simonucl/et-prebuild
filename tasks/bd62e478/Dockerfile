# syntax=docker/dockerfile:1
# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Set up required directory and file
RUN mkdir -p /home/user/provisioning

RUN printf 'APP_ENV=production\nMAX_CONNECTIONS=200\n' > /home/user/provisioning/infra.env

# Adjust permissions
RUN chmod 0777 /home/user/provisioning
RUN chmod 0666 /home/user/provisioning/infra.env

# Apply chmod that was inside %environment
RUN chmod 755 /home/user