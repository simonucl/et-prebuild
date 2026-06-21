# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / description
# Environment for the Mobile-CI error-summary task with pytest pre-installed.
# Author: task-preparer

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    mkdir -p /home/user/mobile_ci

RUN cat > /home/user/mobile_ci/build.log <<'EOF'
2023-07-11 09:14:22 INFO: Starting build for app module
2023-07-11 09:14:24 WARN: Deprecated API usage in Gradle script
2023-07-11 09:14:26 ERROR: Could not locate keystore file 'release.jks'
2023-07-11 09:14:29 ERROR: Missing SDK platform 'android-30'
2023-07-11 09:14:31 INFO: Downloading dependencies
2023-07-11 09:14:45 ERROR: Unable to resolve dependency 'com.google.firebase:firebase-analytics'
2023-07-11 09:14:47 ERROR: Lint found fatal errors in the release build
2023-07-11 09:14:48 INFO: Attempting to continue despite errors
2023-07-11 09:14:50 ERROR: Build failed due to earlier errors
2023-07-11 09:14:52 INFO: Build process finished (took 30 sec)
EOF

RUN chmod 755 /home/user && \
    chmod 0777 /home/user/mobile_ci && \
    chmod 0644 /home/user/mobile_ci/build.log

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

LABEL Author="task-preparer"
LABEL Description="Environment for the Mobile-CI error-summary task with pytest pre-installed."