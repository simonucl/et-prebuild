FROM ubuntu:22.04

# Labels
LABEL Author="automated-setup"
LABEL Description="Container image providing the initial state for the release-directory standardisation task."

# Basic tooling
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Prepare the initial file-system state for the exercise
RUN BASE=/home/user/app && \
    # Create the required directory hierarchy.
    mkdir -p "${BASE}/releases/v1.0.0" && \
    mkdir -p "${BASE}/releases/v1.1.0" && \
    mkdir -p "${BASE}/shared" && \
    mkdir -p "${BASE}/logs" && \
    # Populate README.txt files for the two existing releases.
    printf 'Version 1.0.0\n' > "${BASE}/releases/v1.0.0/README.txt" && \
    printf 'Version 1.1.0\n' > "${BASE}/releases/v1.1.0/README.txt" && \
    # Create the shared configuration file.
    printf 'db: prod\ncache: redis\n' > "${BASE}/shared/config.yml" && \
    # Ensure everything is writable by any unprivileged user who runs the container.
    chmod -R 0777 /home /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Set working directory
WORKDIR /home/user