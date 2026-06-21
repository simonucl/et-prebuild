# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# help: chmod 755 /home/user
# This container provides the starting point for the “purge *.tmp placeholders” exercise.
# Three *.tmp files live somewhere under /home/user/artifacts and must be removed by the learner
# using the prescribed find/xargs one-liner. Pytest is installed so the autograder can verify
# both the initial and final states.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && apt-get update && apt-get install -y --no-install-recommends python3 python3-pip && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/artifacts/repoA/releases && \
    mkdir -p /home/user/artifacts/repoB/snapshots

RUN echo 'binary jar placeholder' > /home/user/artifacts/repoA/releases/libfoo-1.0.jar && \
    echo 'binary jar placeholder' > /home/user/artifacts/repoB/snapshots/libbar-2.3.jar && \
    echo '# Project artifacts' > /home/user/artifacts/readme.md

RUN touch /home/user/artifacts/repoA/releases/unused.tmp && \
    touch /home/user/artifacts/repoA/releases/staging.tmp && \
    touch /home/user/artifacts/repoB/snapshots/cache.tmp

RUN chmod -R a+rwX /home/user