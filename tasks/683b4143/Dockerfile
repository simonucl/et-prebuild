FROM ubuntu:22.04

# Labels
LABEL Author="QA-Task-Builder"
LABEL Description="Base image for SQLite QA testing exercise"

# Refresh package lists and install required tools
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
# Note: chmod in %environment is not valid for ENV, PATH is set instead
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Default action: just execute whatever the user supplied
ENTRYPOINT []
CMD ["/bin/bash"]

# Help information (as comments):
# This container image provides:
#   • Python 3 with pytest
#   • SQLite 3 CLI
# It is intended for a QA exercise where the user will create a local
# SQLite workspace under /home/user/qa_tests/db at runtime.