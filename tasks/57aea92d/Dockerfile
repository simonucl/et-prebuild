# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer %labels
LABEL Author="Apptainer Setup Script for Support-Sim Task"

#------------------------------------------------------------------
# Basic tooling
#------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#------------------------------------------------------------------
# Prepare initial filesystem state expected by the tests
#------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user && \
    BASE="/home/user/support-sim" && \
    mkdir -p "${BASE}/admin" && \
    mkdir -p "${BASE}/logs" && \
    mkdir -p "${BASE}/releases/v1" && \
    mkdir -p "${BASE}/releases/v2" && \
    printf 'version=v1\n' > "${BASE}/releases/v1/app.conf" && \
    printf 'version=v2\n' > "${BASE}/releases/v2/app.conf" && \
    touch "${BASE}/logs/2023-07-28.log" && \
    touch "${BASE}/logs/2023-08-01.log" && \
    touch "${BASE}/logs/2023-08-15.log" && \
    ln -s "${BASE}/releases/v2" "${BASE}/current" && \
    chmod -R a+rwx /home/user && \
    chmod 755 /home/user

#------------------------------------------------------------------
# Environment variables from Apptainer %environment
#------------------------------------------------------------------
ENV PYTHONUNBUFFERED=1

# %help section was not provided in the original definition file