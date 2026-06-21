FROM ubuntu:22.04

# Labels
LABEL Author="archive-utils-setup"
LABEL Description="Environment prepared for the archive-utils exercise. Includes pytest and the initial directory structure."

# Update base system and install Python + pip
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create initial filesystem for the "archive-utils" exercise
# Ensure /home/user exists
RUN mkdir -p /home/user

# Base working directory
RUN mkdir -p /home/user/projects/archive-utils

# Sub-directories
RUN mkdir -p /home/user/projects/archive-utils/alpha && \
    mkdir -p /home/user/projects/archive-utils/beta && \
    mkdir -p /home/user/projects/archive-utils/gamma

# Populate files with required contents (each line ends with newline)
RUN printf 'Alpha file 1\n' > /home/user/projects/archive-utils/alpha/file1.txt && \
    printf 'Alpha file 2\n' > /home/user/projects/archive-utils/alpha/file2.txt && \
    printf 'Beta file 1\n' > /home/user/projects/archive-utils/beta/file1.txt && \
    printf 'Beta file 2\n' > /home/user/projects/archive-utils/beta/file2.txt && \
    printf 'Gamma file 1\n' > /home/user/projects/archive-utils/gamma/file1.txt && \
    printf 'Gamma file 2\n' > /home/user/projects/archive-utils/gamma/file2.txt

# Permissions: allow the non-root runtime user to read/write everything
RUN chmod -R a+rwx /home/user/projects && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user