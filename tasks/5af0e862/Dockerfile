# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# %help
# This container provides:
#   • Python 3 with venv and pip
#   • pytest for automated grading
#   • A writable project directory at /home/user/webapp
#
# Learners will create their own virtual environment and related files inside
# /home/user/webapp as described in the assignment.

ENV DEBIAN_FRONTEND=noninteractive

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/webapp && \
    chmod -R 0777 /home/user

LABEL Author="Apptainer task image generator" \
      Description="Base image for virtual-environment setup exercise"