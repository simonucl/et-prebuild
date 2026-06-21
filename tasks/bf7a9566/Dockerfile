# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python, pip, and pytest
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/data/raw

RUN printf 'Hello world\nMachine learning is fun\nAI\n' \
    > /home/user/data/raw/sample1.txt

RUN printf 'AI\nHello world\nDeep learning\n' \
    > /home/user/data/raw/sample2.txt

RUN chmod -R 777 /home/user/data
RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

LABEL Author="text-corpus-task"
LABEL Version="1.0"
LABEL Description="Initial state for tiny text-corpus preparation optimisation task."