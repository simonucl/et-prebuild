FROM ubuntu:22.04

# Author linux-support-bot
# Description Container prepared for “system snapshot” exercise. Includes Python 3, pytest, and required system utilities.
# Help:
# This container provides the environment required for the “system snapshot” task.
# It includes:
#   • Python 3 (>=3.10)
#   • pytest
#   • Core GNU utilities plus iproute2 (for the `ss` command)
# The home directory /home/user exists and is writable. The diagnostics artefacts
# that the learner must create are purposefully not present.

RUN set -e && \
    echo "Updating package lists..." && \
    apt-get update -y && \
    echo "Installing required Debian/Ubuntu packages..." && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        iproute2 \
        python3-pip && \
    echo "Installing pytest via pip..." && \
    pip3 install --no-cache-dir pytest && \
    echo "Creating /home/user with liberal permissions..." && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    echo "Cleaning up apt caches..." && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# From %environment
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:${PATH}"

CMD ["/bin/bash"]