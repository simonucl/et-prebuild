FROM ubuntu:22.04

# Installer and pytest setup
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare filesystem state
RUN mkdir -p /home/user && \
    chmod 1777 /home/user

RUN printf 'abc' > /home/user/sample_data.txt && \
    chmod 0644 /home/user/sample_data.txt

# Apply chmod from %environment (must be RUN, not ENV)
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Labels
LABEL Author="Backup-Integrity Exercise Builder"

# Help text
# Container image for the “backup integrity” programming assignment.
# Pre-installs pytest and ships the required /home/user/sample_data.txt
# file so that the student can focus solely on writing their solution.