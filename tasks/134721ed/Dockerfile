FROM ubuntu:22.04

# Help text
# This container provides the initial state and dependencies (pytest) for
# the “Create a checksum manifest for curated Java binaries” programming task.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/artifacts/java/plugins && \
    printf 'Sample binary A\n' > /home/user/artifacts/java/libraryA-1.0.jar && \
    printf 'Sample binary B\n' > /home/user/artifacts/java/plugins/pluginB-2.1.jar && \
    chmod -R a+rX /home/user/artifacts

RUN chmod 755 /home/user

LABEL Author="task-setup"
LABEL Description="Environment for the checksum-manifest Apptainer exercise"