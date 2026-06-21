FROM ubuntu:22.04

# Labels
LABEL Author="AI-Generated"
LABEL Task="Filesystem permissions exercise (secure_project)"
LABEL BaseImage="ubuntu:22.04"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create a convenience, non-privileged account called "user"
# (the exercise refers to /home/user explicitly)
RUN if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user || true; \
        useradd -m -u 1000 -g user -s /bin/bash user || true; \
    fi

# Ensure the /home/user directory exists and is writable by whoever
# executes the container (no root/sudo will be available later).
# Sticky-bit (1777) behaves like /tmp: everyone can create but can't
# delete files owned by others.
RUN mkdir -p /home/user && \
    chmod 1777 /home/user

# Environment variables
# Allow user-installed Python tools to be found, if the agent installs any.
ENV PATH="/home/user/.local/bin:${PATH}"

# Note: The chmod 755 /home/user from %environment is moved to a RUN command
# since ENV cannot execute commands. However, this conflicts with the 1777
# permission set above. Keeping the 1777 as it was set in %post.

# Help: Container for the "secure_project" permissions exercise.
# Python 3 and pytest are installed; no secure_project content exists yet.