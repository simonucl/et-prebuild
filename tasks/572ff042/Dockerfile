# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Labels
# ------------------------------------------------------------------
LABEL Author="IoT-Fleet exercise preparer"
LABEL Description="Base image containing the initial state for the IoT fleet maintenance task."

# ------------------------------------------------------------------
# 1. Install Python tooling needed for the grader
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# 2. Prepare the initial IoT-fleet workspace
# ------------------------------------------------------------------
RUN set -e && \
    BASE="/home/user/iot_fleet" && \
    mkdir -p "${BASE}/firmware_packages" && \
    mkdir -p "${BASE}/devices_info" && \
    mkdir -p "${BASE}/deployment_logs" && \
    \
    echo "dummy firmware sensorA v1.2"  > "${BASE}/firmware_packages/sensorA_v1.2.fw" && \
    echo "dummy firmware sensorA v3.1"  > "${BASE}/firmware_packages/sensorA_v3.1.fw" && \
    echo "dummy firmware camB v2.9"     > "${BASE}/firmware_packages/camB_v2.9.fw" && \
    echo "dummy firmware camB v3.0"     > "${BASE}/firmware_packages/camB_v3.0.fw" && \
    echo "dummy firmware gateway v2.5"  > "${BASE}/firmware_packages/gateway_v2.5.fw" && \
    echo "dummy firmware gateway v3.2"  > "${BASE}/firmware_packages/gateway_v3.2.fw" && \
    \
    yes '{"dummy":"sensorA"}' | head -c 1500 > "${BASE}/devices_info/sensorA.json" && \
    yes '{"dummy":"camB"}'    | head -c 800  > "${BASE}/devices_info/camB.json" && \
    yes '{"dummy":"gateway"}' | head -c 2048 > "${BASE}/devices_info/gateway.json" && \
    yes '{"dummy":"edgeHub"}' | head -c 3000 > "${BASE}/devices_info/edgeHub.json" && \
    \
    chmod -R a+rwx /home/user/iot_fleet

# ------------------------------------------------------------------
# Environment setup
# ------------------------------------------------------------------
RUN chmod 755 /home/user
ENV PYTHONUNBUFFERED=1

# ------------------------------------------------------------------
# Help
# ------------------------------------------------------------------
# This image provides the starting filesystem layout and files
# for the IoT-fleet batch-deployment exercise.