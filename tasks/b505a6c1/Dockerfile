FROM ubuntu:22.04

# --------------------------------------------------------------------- #
# Basic OS packages
# --------------------------------------------------------------------- #
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------- #
# Python tooling (pytest for the evaluation harness)
# --------------------------------------------------------------------- #
RUN pip3 install --no-cache-dir pytest

# --------------------------------------------------------------------- #
# Prepare the initial Git repository that the agent will work in
# Path: /home/user/experiments/model-training
# --------------------------------------------------------------------- #
# Create directory structure
RUN mkdir -p /home/user/experiments/model-training

# Create README.md with the required single line + newline
WORKDIR /home/user/experiments/model-training
RUN echo "Model training experiments" > README.md

# Initialise Git repository with main branch
RUN git init -b main

# Configure dummy author information so the initial commit can be made
RUN git config user.name "Container Builder" && \
    git config user.email "builder@example.com"

# Stage and commit README.md
RUN git add README.md && \
    git commit -m "Initial commit with README.md"

# --------------------------------------------------------------------- #
# Permissions: make repository world-writable so the non-root runtime
# user can create tags, log files, etc.
# --------------------------------------------------------------------- #
RUN chmod -R a+rwX /home/user/experiments

RUN chmod 755 /home/user

# Labels
LABEL Author="MLOps-Container-Builder"
LABEL Description="Container for Git tagging task – provides initial repo state and pytest"

# Help information (as comment):
# This container delivers an initial Git repository located at
#   /home/user/experiments/model-training
# with a committed README.md on branch 'main' and no tags.
# Pytest is pre-installed to allow the automated grading suite to run.

WORKDIR /home/user