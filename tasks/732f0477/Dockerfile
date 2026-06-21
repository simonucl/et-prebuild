# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: ChatGPT
# Description: Seed environment for Git deployment task with initial bare repo and pytest installed.

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN set -eux && \
    mkdir -p /home/user/remote && \
    TEMP_WORK=/tmp/sample-app-seed && \
    mkdir -p "${TEMP_WORK}" && \
    cd "${TEMP_WORK}" && \
    git init && \
    git config user.name "Builder" && \
    git config user.email "builder@example.com" && \
    printf "2.0.0\n" > VERSION && \
    git add VERSION && \
    git commit -m "Initial version 2.0.0" && \
    git branch -M main && \
    git clone --bare . /home/user/remote/sample-app.git && \
    git --git-dir=/home/user/remote/sample-app.git symbolic-ref HEAD refs/heads/main && \
    cd / && \
    rm -rf "${TEMP_WORK}"

RUN chmod -R a+rX /home/user && \
    chmod 755 /home/user

ENV PATH="/home/user/.local/bin:${PATH}"

LABEL Author="ChatGPT" \
      Description="Seed environment for Git deployment task with initial bare repo and pytest installed."