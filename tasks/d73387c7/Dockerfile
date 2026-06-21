FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Preparer"
LABEL Description="Environment for directory-reorganisation task; includes pytest and required starter files."

# Install Python tooling needed for the tests
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the initial workspace expected by the assignment
RUN mkdir -p /home/user/workspace

# Create intro.md
RUN cat >/home/user/workspace/intro.md <<'EOF'
# Introduction
Placeholder content for intro.md
EOF

# Create api.md
RUN cat >/home/user/workspace/api.md <<'EOF'
# API
Placeholder content for api.md
EOF

# Create style.md
RUN cat >/home/user/workspace/style.md <<'EOF'
# Style Guide
Placeholder content for style.md
EOF

# Create guide.txt
RUN cat >/home/user/workspace/guide.txt <<'EOF'
Guide content placeholder for guide.txt
EOF

# Make sure the unprivileged runtime user can freely modify
# everything inside /home/user and below.
RUN chmod -R 777 /home/user

# Clean up apt caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

# Set working directory
WORKDIR /home/user