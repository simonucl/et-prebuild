FROM ubuntu:22.04

# Author incident-response-task
# Description "Base image for DNS incident response exercise"
# Help:
#   This container provides the baseline environment for the “DNS incident response” exercise.
#   It guarantees:
#     - /home/user exists (but no incidents directory yet).
#     - At least one DNS utility (dig) is available.
#     - pytest is installed for automated grading.

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

RUN set -e && \
    echo "Updating package lists..." && \
    apt-get update && \
    echo "Installing DNS utilities and Python tooling..." && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        dnsutils \
        python3 \
        python3-pip && \
    echo "Installing pytest..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    echo "Creating /home/user directory..." && \
    mkdir -p /home/user && \
    chmod 755 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD echo "Container ready for DNS incident response exercise." && \
    echo "Start an interactive shell with: docker run -it <image> /bin/bash"