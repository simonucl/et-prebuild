FROM ubuntu:22.04

# Help documentation:
# This container image provides the starting filesystem required for the
# "payment_api" incident-response task. Both mock containers start in the
# RUNNING state and pytest is available for automated grading.

# Basic packages
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip

# Install pytest for the grader and the student
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial filesystem layout required by the task description
# ------------------------------------------------------------------

# Create mock container runtime directories
RUN mkdir -p /home/user/mock_docker/containers/payment_api && \
    mkdir -p /home/user/mock_docker/containers/web_frontend

# Populate status.txt files with the initial state "RUNNING"
RUN echo -n "RUNNING" > /home/user/mock_docker/containers/payment_api/status.txt && \
    echo -n "RUNNING" > /home/user/mock_docker/containers/web_frontend/status.txt

# Ensure everything under /home/user is writable by any UID that will
# execute inside the container (the grading agent runs as an
# unprivileged user whose UID we don't know in advance).
RUN chmod -R a+rwX /home/user

LABEL Author="YourName"
LABEL Description="Environment for operations triage exercise – mock container runtime pre-populated."