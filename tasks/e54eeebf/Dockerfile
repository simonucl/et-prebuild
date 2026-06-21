FROM ubuntu:22.04

# Labels
LABEL Author="ExampleCourse"
LABEL Description="Environment for the 'Symbolic-link housekeeping for an API integration sandbox' exercise."

# Help: This container supplies the initial filesystem state and tools (Python,
# pytest) required for the symbolic-link housekeeping exercise.

# Basic tooling
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare the initial state expected by the exercise's test-suite.
# 1. Create the directory hierarchy for the in-house API versions.
RUN mkdir -p /home/user/apis/v1.2.3

# 2. Make sure the student (a non-root UID at runtime) can modify
#    everything inside /home/user without privilege escalation.
RUN chmod -R 0777 /home/user

# Environment variables
ENV PYTHONUSERBASE=/home/user/.local
ENV PATH="$PYTHONUSERBASE/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Set permissions on container start (note: chmod in %environment runs at runtime)
# For Docker, we ensure permissions are set during build
RUN chmod 755 /home/user