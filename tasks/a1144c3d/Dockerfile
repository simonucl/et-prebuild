FROM ubuntu:22.04

# Labels
LABEL Author="backup-exercise"
LABEL Description="Environment prepared for Markdown documentation backup exercise"

# Update package index and install Python along with pytest
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the documentation directory
RUN mkdir -p /home/user/documentation

# Ensure the future backup location can be created by an unprivileged user
RUN chmod 777 /home/user

# Populate the three required Markdown files with exact content
RUN cat > /home/user/documentation/overview.md <<'EOF'
# Project Overview
This document provides a bird-eye summary of the project.
EOF

RUN cat > /home/user/documentation/getting_started.md <<'EOF'
# Getting Started
Step-by-step guide to install and configure the project.
EOF

RUN cat > /home/user/documentation/api_reference.md <<'EOF'
# API Reference
Exhaustive list of endpoints, parameters and response formats.
EOF

# Set sensible permissions
RUN chmod 755 /home/user/documentation && \
    chmod 644 /home/user/documentation/*.md

# Help information (as comments):
# This container provides the starting filesystem layout for the
# "version-locked Markdown backup" task.