# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state expected by the tests
RUN mkdir -p /home/user/builds/artifacts

# Create the three JAR artifacts with the exact byte-sizes required
RUN printf 'CORE_1.2.0_CONTENT\n'           > /home/user/builds/artifacts/app-core-1.2.0.jar
RUN printf 'CORE_1.2.1_SNAPSHOT_CONTENT\n'  > /home/user/builds/artifacts/app-core-1.2.1-SNAPSHOT.jar
RUN printf 'UI_1.2.0_CONTENT\n'             > /home/user/builds/artifacts/app-ui-1.2.0.jar

# Ensure world-readable permissions so non-root users can access them
RUN chmod -R a+rX /home/user

# %environment section
RUN chmod 755 /home/user
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8