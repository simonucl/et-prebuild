# Help:
# This container supplies the minimal environment needed for the learner to
# complete the data pre-processing exercise.
# Python 3 and pytest are pre-installed, and /home/user is ready for use.

FROM ubuntu:22.04

# Labels
LABEL Author="Your Name"
LABEL Description="Starter container for the data pre-processing environment. Includes Python and pytest, with a clean workspace at /home/user."

# Install Python, pip, pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create the expected home directory
RUN mkdir -p /home/user && chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Default behavior is to run whatever command is passed, so no ENTRYPOINT needed