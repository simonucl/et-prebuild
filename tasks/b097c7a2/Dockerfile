# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help text from %runscript
# Container for release-manager exercise. Open a shell with:
#   apptainer exec <container.sif> /bin/bash

ENV PYTHONUNBUFFERED=1

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    USER_HOME="/home/user" && \
    mkdir -p "$USER_HOME/artifacts" && \
    mkdir -p "$USER_HOME/releases" && \
    mkdir -p "$USER_HOME/deployments" && \
    chmod 0777 "$USER_HOME" && \
    chmod 0777 "$USER_HOME/deployments"

RUN set -e && \
    USER_HOME="/home/user" && \
    printf 'DUMMY CONTENT FOR app1 version 1.2.3\n' > "$USER_HOME/artifacts/app1_v1.2.3.tar.gz" && \
    printf 'DUMMY CONTENT FOR app2 version 0.9.8\n' > "$USER_HOME/artifacts/app2_v0.9.8.tar.gz" && \
    printf 'DUMMY CONTENT FOR app3 version 3.4.5\n' > "$USER_HOME/artifacts/app3_v3.4.5.tar.gz"

RUN set -e && \
    USER_HOME="/home/user" && \
    RELEASE_CSV="$USER_HOME/releases/release_2023-10-15.csv" && \
    printf 'app,version,artifact_file\n' > "$RELEASE_CSV" && \
    printf 'app1,1.2.3,%s/app1_v1.2.3.tar.gz\n' "$USER_HOME/artifacts" >> "$RELEASE_CSV" && \
    printf 'app2,0.9.8,%s/app2_v0.9.8.tar.gz\n' "$USER_HOME/artifacts" >> "$RELEASE_CSV" && \
    chmod 755 /home/user