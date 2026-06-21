# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="IoT-Edge-Prep"
LABEL Description="Container providing the initial state for the IoT firmware bundling task"

# Install python and pytest, and set up seed data
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        --no-install-recommends && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/* && \
    \
    # ------------------------------------------------------------------
    # Seed data required by the assignment’s initial state
    # ------------------------------------------------------------------
    # Create the /home/user hierarchy (no user creation needed)
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    \
    # Create the single-byte firmware seed file (contains ASCII “a” only)
    printf 'a' > /home/user/sample_firmware_v1.2.bin && \
    chmod 644 /home/user/sample_firmware_v1.2.bin

# Environment variables from %environment
ENV PYTHONUNBUFFERED=1

# %help
# This container includes:
#   • Ubuntu 22.04 base system
#   • pytest for automated grading
#   • A seed file at /home/user/sample_firmware_v1.2.bin (1 byte, “a”)
# Students will perform actions inside this filesystem to complete the task.