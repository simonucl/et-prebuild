FROM ubuntu:22.04

# Labels
LABEL Author="student-setup"
LABEL Description="Container for release-notes tidy-up exercise"

# Update package list and install required system packages
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        patch \
        diffutils \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pytest for the grading harness
RUN pip3 install --no-cache-dir pytest

# Prepare initial workspace expected by the assignment
RUN mkdir -p /home/user/docs

# Create the initial, unpatched user_guide.md file (7 lines, LF endings)
RUN cat <<'EOF' >/home/user/docs/user_guide.md
# MyApp User Guide v1.0

Welcome! In this document you will learn how to instal and configure MyApp.

To recieve updates, subscribe to our newsletter.

Happy hacking!
EOF

# Ensure the agent has write permissions to create patches and logs
RUN chmod 777 /home/user/docs && \
    chmod 666 /home/user/docs/user_guide.md && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C

# Help information (as comment)
# This container image provides the initial filesystem state required for
# the release-notes tidy-up task.