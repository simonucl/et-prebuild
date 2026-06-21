FROM ubuntu:22.04

# Help / runscript comments
# This container sets up the initial state for the checksum task.
# Use 'apptainer exec' with your own command to work inside the container.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/docs && \
    chmod 0777 /home/user/docs && \
    : > /home/user/docs/faq.md && \
    : > /home/user/docs/introduction.md && \
    : > /home/user/docs/usage-guide.md && \
    chmod 0644 /home/user/docs/*.md

RUN chmod 755 /home/user || true

LABEL Author="ChatGPT Task Preparer"
LABEL Description="Container with initial state for checksum generation task."