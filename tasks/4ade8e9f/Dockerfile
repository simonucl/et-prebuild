# Converted from Apptainer definition file
FROM ubuntu:22.04

# Post section
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-venv \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment section
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Labels section
LABEL Author="Container build script for perf_venv task"

# Help section (comments)
# This image provides a minimal Ubuntu 22.04 environment with:
#   - Python 3 and the venv module
#   - pip, setuptools, wheel
#   - pytest (required by the automated grader)
# The container intentionally does NOT create /home/user/perf_venv/
# so that the student can perform the required steps during assessment.