FROM ubuntu:22.04

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare writable workspace for the student
RUN mkdir -p /home/user && chmod 0777 /home/user

# Labels
LABEL Author="AutomationExercise"
LABEL Description="Container for workflow.service single-command task with pytest pre-installed."