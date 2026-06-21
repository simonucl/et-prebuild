FROM ubuntu:22.04

# Update package index and install build tools plus Python & pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare initial exercise filesystem layout
# ------------------------------------------------------------------
# Create /home/user/old_code and make it writable for any unprivileged user
RUN mkdir -p /home/user/old_code && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/old_code

# Place the legacy source file. Do NOT create the build artefacts.
RUN cat <<'EOF' > /home/user/old_code/legacy_hello.c
#include <stdio.h>

int main(void)
{
    puts("HELLO_FROM_1999");
    return 0;
}
EOF

RUN chmod 0644 /home/user/old_code/legacy_hello.c && \
    chmod 755 /home/user

# Author: legacy-container-setup
# Description: Environment for compiling and testing legacy_hello.c
#
# Help:
# This container provides the starting state for the "legacy_hello" exercise.
# The source file is located in /home/user/old_code/legacy_hello.c.
# No executable or log file is present; the learner must create them.
# Python with pytest is installed for automated grading.