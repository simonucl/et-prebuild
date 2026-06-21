# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="deploybot-setup"
LABEL Description="Container for CI/CD identity-file exercise – initial state preparation"

# Update package list and install Python tooling
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip python3-setuptools ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ---------------------------------------------------------------------
# Prepare initial filesystem state expected by the exercise test suite
# ---------------------------------------------------------------------
# 1. Create the working directory tree
RUN mkdir -p /home/user/ci_access

# 2. Populate users.csv with the two starter lines, each ending with \n
RUN printf 'alice,ci-viewers\nbob,ci-operators\n' > /home/user/ci_access/users.csv

# 3. Ensure the student (non-root runtime user) has full write access
RUN chmod 777 /home/user/ci_access && \
    chmod 666 /home/user/ci_access/users.csv

# Ensure correct permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Default command (container is for assessment)
CMD ["bash"]