# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Labels from Apptainer %labels section
# ------------------------------------------------------------------
LABEL Author="MLOps-Quadratic-Setup"
LABEL Description="Environment for quadratic optimisation artifact exercise (includes pytest)"

# ------------------------------------------------------------------
# Install Python tooling and pytest for the checker
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial experiment state expected by the automatic tests
# ------------------------------------------------------------------
RUN set -e && \
    mkdir -p /home/user/experiments/quadratic_coeffs && \
    printf "2 -8 3\n" > /home/user/experiments/quadratic_coeffs/coefficients.txt && \
    chmod 755 /home/user && \
    chmod -R 755 /home/user/experiments && \
    chmod 644 /home/user/experiments/quadratic_coeffs/coefficients.txt

# ------------------------------------------------------------------
# Environment variables from Apptainer %environment section
# ------------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8