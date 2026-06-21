FROM ubuntu:22.04

# Labels
LABEL Author="AI-Generated"
LABEL Description="Starter container for Makefile-authoring assignment"

# Basic development tool-chain and Python/pytest
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        time \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the starter project skeleton
RUN mkdir -p /home/user/project/src

# Create main.c file
RUN cat <<'EOF' > /home/user/project/src/main.c
#include <stdio.h>

int main(void)
{
    puts("Hello, performance world!");
    return 0;
}
EOF

# Give write permission to anyone so the unprivileged agent can work
RUN chmod -R 777 /home/user

# Environment setup
ENV HOME=/home/user

# Set working directory
WORKDIR /home/user/project

# Default command
CMD ["/bin/bash"]

# Help information (as comments):
# This container supplies the minimal starter state for the Makefile
# assignment.  Only the file
#
#     /home/user/project/src/main.c
#
# exists at build time.  The student is expected to author a Makefile
# and create further artefacts during the assessment workflow.