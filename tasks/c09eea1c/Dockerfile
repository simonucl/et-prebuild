FROM ubuntu:22.04

# Author: log_analysis_container
# Description: Base environment for log_review_env exercise – includes Python, venv support, and pytest.

# Help:
# This container provides a pristine Ubuntu 22.04 environment with Python 3,
# the standard 'venv' module, and pytest pre-installed.  It intentionally
# does NOT contain /home/user/log_review_env so that students can create
# the virtual environment themselves during the exercise.

# Update package index and install Python (with venv support) plus utilities
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        python-is-python3 \
        ca-certificates \
        build-essential

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Ensure the expected home directory exists
RUN mkdir -p /home/user && \
    chmod 755 /home/user

# Clean up apt caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"