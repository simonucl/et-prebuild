FROM ubuntu:22.04

# Labels
LABEL Author="DeployTaskSetup"
LABEL Description="Initial state for data-pipeline rollout exercise"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare filesystem required by the task
RUN mkdir -p /home/user/data-pipeline/releases/v1.9 && \
    mkdir -p /home/user/data-pipeline/releases/v2.0

# Version marker files (must end with newline)
RUN printf '1.9\n' > /home/user/data-pipeline/releases/v1.9/VERSION && \
    printf '2.0\n' > /home/user/data-pipeline/releases/v2.0/VERSION

# Symlink that initially points to the old release
RUN ln -s /home/user/data-pipeline/releases/v1.9 /home/user/data-pipeline/current

# Roll-out log with only the header line
RUN printf 'timestamp,from,to,status\n' > /home/user/rollout.log

# Make everything under /home/user writable so the unprivileged agent
# can perform the required updates during testing.
RUN chmod -R a+rwx /home/user

# Set working directory
WORKDIR /home/user

# Default entrypoint
CMD ["chmod", "755", "/home/user"]