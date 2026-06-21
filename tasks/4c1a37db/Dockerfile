FROM ubuntu:22.04

# Help:
# Base container for the “Quick API Diagnostic” exercise.
# Includes curl, Python 3, and pytest, plus the pre-populated JSON
# files required by the assessment.

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages and pytest
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create directory structure and JSON files
RUN mkdir -p /home/user/data && \
    chmod 0777 /home/user && \
    echo '{"status":"ok"}' > /home/user/data/status.json && \
    echo '{"version":"1.3.7"}' > /home/user/data/version.json && \
    chmod 0644 /home/user/data/status.json /home/user/data/version.json

# Labels
LABEL Author="quick-api-diagnostic-container"